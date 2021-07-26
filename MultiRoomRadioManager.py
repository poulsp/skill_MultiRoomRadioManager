#  Copyright (c) 2021 Poul Spang
#
#  This file, MultiRoomRadioManager.py, is part of Project skill_MultiRoomRadioManager.
#
#  Project skill_MultiRoomRadioManager is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>


# ~/.local/bin/projectalice-sk validate --paths ~/ProjectAlice/skills/MultiRoomRadioManager

import requests
from enum import IntEnum
from os import path
import json
import subprocess

from core.commons import constants
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from core.util.Decorators import MqttHandler


from skills.MultiRoomMediaVolume.library.Topics import(	_MULTIROOM_ENTRY_VOLUME,
																												_MULTIROOM_STREAM_STOP,
																												_MULTIROOM_PLAYER_PLAY,
																												_MULTIROOM_PLAYER_STOP,
																												_MULTIROOM_STREAM_STOPPED,
																												_MULTIROOM_BLUETOOTH_STREAM_STOP,
																												_MULTIROOM_RADIO_UPDATE_RADIOSTATIONS,
																												_MULTIROOM_QUERY_RADIO_RADIOSTATIONS,
																												_MULTIROOM_SEND_RADIO_RADIOSTATIONS,
																												_RADIOMANAGER_WIDGET_REFRESH,
																												_UNKNOWN_RADIO_STATION
																											)


from skills.MultiRoomRadioManager.library.CheckWeb import(CheckNodejs)
from skills.MultiRoomRadioManager.library.WebRadioManager import(WebRadioManager)


ROOM_TEST = False

class RadioStation(IntEnum):
	STATION_NAME = 0
	VOLUME       = 1
	STATION_URL  = 2
	ONLINE       = 3


#-----------------------------------------------
class MultiRoomRadioManager(AliceSkill):
	"""
	Author: poulsp
	Description: Manage internet radio stations and players in the synchronous multiroom audio system.
	"""

	NAME = 'MultiRoomRadioManager'

	#-----------------------------------------------
	def __init__(self):
		super().__init__()

		self._baseServer        = constants.DEFAULT

		self.RADIO_STATIONS = {}
		self.radioStations      = dict()
		self._stationCurrent    = _UNKNOWN_RADIO_STATION
		self._stationName       = ""
		self._playing           = False
		self._rooms             = list()
		self.playEverywhereAsDefault = False
		self._sendOutWhiteNoise = False
		self._sendingWhiteNoise = False

		#TODO Get Speaker work again.
		self.speaker = None
		#self._speaker = Speaker()

		self._ffMpegNamedpipe = None


	#-----------------------------------------------
	@property
	def rooms(self):
		return self._rooms


	#-----------------------------------------------
	def onStart(self):
		super().onStart()

		if not path.exists('./skills/MultiRoomRadioManager/radio_stations.json'):
			cmd = 'cp ./skills/MultiRoomRadioManager/radio_stations.json.sample ./skills/MultiRoomRadioManager/radio_stations.json'
			subprocess.call(cmd, shell=True)


		self._readRadioStations()
		self.playEverywhereAsDefault = self.getConfig('playEverywhereAsDefault')

		self._setDNDWhenStartPlaying = self.getConfig('setDNDWhenStartPlaying')
		self._dndTopic = self.getConfig('dndTopic').strip()

		self._rooms = self.getConfig('rooms')
		self._rooms = self._rooms.split(',')
		for i in range(len(self._rooms)):
			self._rooms[i] = self._rooms[i].strip()
		self._rooms.append(self._baseServer)
		self._rooms.append("everywhere")

		if ROOM_TEST:
			self._rooms = self._rooms + ['everywhere','all','all locations','base','cellar','basement','dining room','entrance','kitchen','laundry','lounge','bedroom','outdoor','pantry','office','toilet']

		# Delete all duplicates
		self._rooms = list(dict.fromkeys(self._rooms))

		self._sendingWhiteNoise = False
		self._sendOutWhiteNoise = self.getConfig('sendOutWhiteNoise')
		if (self._sendOutWhiteNoise):
			# Write self._sendOutWhiteNoise back to config set to False
			try:
				self.ConfigManager.updateSkillConfigurationFile('MultiRoomRadioManager', 'sendOutWhiteNoise', 'false')
			except Exception as e:
				raise e

			self._sendOutWhiteNoise = False



		self._ffMpegNamedpipe = "/dev/shm/snapfifo"

		# if self.getConfig('useSpeaker'):
		#   topic = self.getConfig('SpeakerTopic')
		#   OnOff = self.getConfig('SpeakerOnOff')
		# MaxSpeakerIdleMinutes = self.getConfig('MaxSpeakerIdleMinutes')

		#   self.speaker = Speaker(speakerTopic: str ,OnOff: {'on': 'true', 'on': 'false'}, MaxSpeakerIdleMinutes = 30)

		# Don't affect Alice startup time, so we lift off here.
		# self.ThreadManager.doLater(interval=0.2, func=self.delayedInitialize)
		self.delayedInitialize()


	#-----------------------------------------------
	def delayedInitialize(self):
		if CheckNodejs.test4Nodejs():
			CheckNodejs.checkNodeModules(self)
			pass
		else:
			CheckNodejs.installNodejs()
			CheckNodejs.checkNodeModules(self)

		webRadioManagerPort = self.getConfig('webRadioManagerPort')

		apiPort = self.ConfigManager.getAliceConfigByName('apiPort')
		aliceWebInterfacePort = self.ConfigManager.getAliceConfigByName('webInterfacePort')
		adminPinCode = self.ConfigManager.getAliceConfigByName('adminPinCode')
		apiToken, aliceIp = self._getFromApi(adminPinCode)
		self._webRadioManager = WebRadioManager(self, aliceIp, webRadioManagerPort, aliceWebInterfacePort, apiPort, apiToken)
		self._webRadioManager.checkConfig()
		self._webRadioManager.startWebserver()


	#-----------------------------------------------
	def _getFromApi(self, adminPinCode):
		url = 'http://localhost:5001/api/v1.0.1/login/'
		headers = {}
		payload = {
			"username": "admin",
			"pin": adminPinCode
		}

		response = requests.request('POST', url, data=payload, headers=headers)
		apiToken = json.loads(response.text)['apiToken']

		url = 'http://localhost:5001/api/v1.0.1/utils/config/'
		headers = {
			"auth": apiToken
		}

		response = requests.request('GET', url, headers=headers)
		aliceIp = json.loads(response.text)['config']['aliceIp']

		return (apiToken, aliceIp)


	#-----------------------------------------------
	def onStop(self):
		self._webRadioManager.stopWebserver()


	#-----------------------------------------------
	def onDeleted(self):
		super().onDeleted()
		# # TODO evt. fjern nvm og dermed også _exportCmd i ~/.bashrc
		# if self.getConfig('autoRemoveNodejs'):
		# 	CheckNodejs.removeNodejs()



	#-----------------------------------------------
	def setRooms(self, rooms):
		self._rooms = rooms
		self._rooms = self._rooms.split(',')
		for i in range(len(self._rooms)):
			self._rooms[i] = self._rooms[i].strip()
		self._rooms.append(self._baseServer)
		self._rooms.append("everywhere")

		# Delete all duplicates
		self._rooms = list(dict.fromkeys(self._rooms))

		return True


	#-----------------------------------------------
	def _saveRadioStations(self, radioList):
		with open('./skills/MultiRoomRadioManager/radio_stations.json', 'w') as json_file:
			json.dump(radioList, json_file, sort_keys=True, indent=2 )

		self.publish(_RADIOMANAGER_WIDGET_REFRESH, 'dummy')


	#-----------------------------------------------
	def _readRadioStations(self):
		with open("./skills/MultiRoomRadioManager/radio_stations.json", "r") as read_file:
			data = json.load(read_file)

		self.RADIO_STATIONS = data


	#-----------------------------------------------
	@MqttHandler(_MULTIROOM_RADIO_UPDATE_RADIOSTATIONS)
	def _updateRadioStationsHandler(self, session: DialogSession, **_kwargs):
		self._saveRadioStations(session.payload)
		self._readRadioStations()


	#-----------------------------------------------
	@MqttHandler(_MULTIROOM_QUERY_RADIO_RADIOSTATIONS)
	def _ask4RadioStationsHandler(self, session: DialogSession, **_kwargs):
		self.publish(_MULTIROOM_SEND_RADIO_RADIOSTATIONS, json.dumps({'radioStations': self.RADIO_STATIONS}), qos=1)


	#-----------------------------------------------
	@MqttHandler('psp/get/aliceCore/uuid')
	# Used by webRadio to send an api/v1.0.1/dialog/process
	def _getUUID(self, session: DialogSession, **_kwargs):
		deviceUid = self.ConfigManager.getAliceConfigByName('uuid')
		self.publish('psp/aliceCore/deviceUid', json.dumps({"deviceUid": deviceUid}))


	#-----------------------------------------------
	@property
	def _stationInfo(self):
		if self._stationCurrent in self.RADIO_STATIONS:
			stationName   = self.RADIO_STATIONS[self._stationCurrent][RadioStation.STATION_NAME]
			# stationUrl    = self.RADIO_STATIONS[self._stationCurrent][RadioStation.STATION_URL]
			# stationVolume = self.RADIO_STATIONS[self._stationCurrent][RadioStation.VOLUME].strip()[:-1]
		else:
			stationName = _UNKNOWN_RADIO_STATION

		return stationName


	#-----------------------------------------------
	def _startRadioStreamer(self, stationUrl, radioStation, stationName):
		# Power off bluetooth so we are sure the audio is free.
		self.publish(_MULTIROOM_BLUETOOTH_STREAM_STOP, json.dumps({'dummy': 'Dummy'}))

		self._playing = True
		ffmpegCmd =  f"ffmpeg -v 0 -y -rtbufsize 15M -i {stationUrl} -f u16le -acodec pcm_s16le -ac 2 -ar 48000 {self._ffMpegNamedpipe} > /dev/null 2>&1 &"
		subprocess.call(ffmpegCmd, shell=True)


	#-----------------------------------------------
	def _checkFifo(self):
		try:
			_output = subprocess.check_output(
				"ls -l /dev/shm/snapfifo | awk '{print $5}'",
				stderr=subprocess.STDOUT,
				shell=True
			).decode('utf-8').replace('\n','')

			if _output == "ls: cannot access '/dev/shm/snapfifo': No such file or directory":
				mkfifoCmd ="mkfifo /dev/shm/snapfifo -m666"
				subprocess.call(mkfifoCmd, shell=True)
				return

			elif int(_output) > 0:
				removeFifoCmd ="rm /dev/shm/*fifo"
				subprocess.call(removeFifoCmd, shell=True)
				restartSnapserverCmd ="sudo systemctl restart snapserver"
				subprocess.call(restartSnapserverCmd, shell=True)

		except subprocess.CalledProcessError as e:
			raise e


	#-----------------------------------------------
	def _stopFfmpeg(self):
		cmdKill = "/usr/bin/killall -2 ffmpeg >/dev/null 2>&1"
		if self._playing:
			subprocess.call(cmdKill, shell=True)

		# This is more a symptom treatment than a cure.
		# Sometimes it let snapfifo growth.
		# TODO investigate
		self._checkFifo()


	#-----------------------------------------------
	def _stop(self, playSite=None):
		if playSite:
			self.publish(_MULTIROOM_PLAYER_STOP,  json.dumps({'playSite': playSite}))
		else:
			self.publish(_MULTIROOM_PLAYER_STOP,  json.dumps({'playSite': 'everywhere'}))
			self._stopFfmpeg()
			self._playing = False


	#-----------------------------------------------
	@IntentHandler('playRadio')
	def playRadio(self, session: DialogSession, **_kwargs):
		if self._sendOutWhiteNoise:
			self.endDialog(session.sessionId, '')
			return

		thisSideId = self._baseServer
		try:
			station  = None if 'Station' not in session.slots else session.slotValue('Station')
			playSite = 'base' if 'Room' not in session.slots else session.slotValue('Room').lower()

			if self.playEverywhereAsDefault:
				playSite = "everywhere"

			if not playSite in self._rooms or station is None or not isinstance(station, float):
				self._error(session.sessionId, 'errorSlotPlaySiteNotInRooms')
				return

			if not station:
				self._error(session.sessionId, 'errorSlotNoStation')
				return

			radioStation = "radio " + str(int(station))

			if radioStation in self.RADIO_STATIONS:
				stationName   = self.RADIO_STATIONS[radioStation][RadioStation.STATION_NAME]
				stationUrl    = self.RADIO_STATIONS[radioStation][RadioStation.STATION_URL]
				stationVolume = self.RADIO_STATIONS[radioStation][RadioStation.VOLUME].strip()[:-1]
				stationOnline = self.RADIO_STATIONS[radioStation][RadioStation.ONLINE]


				self._stop()
				if (not stationOnline):
					self._playing = False

					self.endDialog(session.sessionId, self.randomTalk('offline', [radioStation]))
					return

				# If off, turn on speaker. TODO Must be uncomment in production.
				#self.speaker.turnOnOff(True)

				self._playing = True

				self._stationCurrent = radioStation
				self._stationName = stationName

				self.publish(_MULTIROOM_ENTRY_VOLUME, json.dumps({'activeSoundApp': self.name,'stationVolume': stationVolume}))

				self._startRadioStreamer(stationUrl, radioStation, stationName)

				if playSite == 'base': # No playSite specified are None
					self.publish(_MULTIROOM_PLAYER_PLAY, json.dumps({'siteId': thisSideId, 'playSite': self._baseServer}))

				elif playSite == 'everywhere':
					self.publish(_MULTIROOM_PLAYER_PLAY, json.dumps({'siteId': thisSideId, 'playSite': 'everywhere'}))

				else:
					self.publish(_MULTIROOM_PLAYER_PLAY, json.dumps({'siteId': thisSideId, 'playSite': playSite}))

				radioPlayingNow = [self._stationCurrent, self._stationName]

				self.endDialog(session.sessionId, self.randomTalk('radioPlaying', radioPlayingNow))

				if self._setDNDWhenStartPlaying:
					self.publish(self._dndTopic, '')

			else:
				self._playing = False
				self._stationCurrent = _UNKNOWN_RADIO_STATION
				self._error(session.sessionId, 'errorSlotStationNotExist')
				return

		except Exception as e:
			print(f"Exception - {e}")
			self._error(session.sessionId, 'errorSlotException')


	#-----------------------------------------------
	@IntentHandler('stopRadio')
	def stopRadio(self, session: DialogSession):
		playSite 	= None if 'Room' not in session.slots else session.slots['Room']

		# Turns off the speaker after a number of minutes, defined in the speaker.py MAXSPEAKERIDLE.
		#self.speaker.idle()

		if self._playing:
			if playSite:
				self._stop(playSite)
				self.endDialog(session.sessionId, '')

			elif (self._stationCurrent in self.RADIO_STATIONS):
				# stationName = self.RADIO_STATIONS[self._stationCurrent][RadioStation.STATION_NAME]

				self._stop()
				self._stationCurrent = _UNKNOWN_RADIO_STATION
				self.endDialog(session.sessionId, self.randomTalk('endStreamingRadio'))

		else:
			self._stop()
			self.endDialog(session.sessionId, self.randomTalk('stationErrorInfo'))


	#-----------------------------------------------
	@MqttHandler(_MULTIROOM_STREAM_STOP)
	def _stopRadioStreamer(self, session: DialogSession, **_kwargs):
		self._stop()
		self.publish(_MULTIROOM_STREAM_STOPPED, json.dumps({'dummy': 'Dummy'}))


	#-----------------------------------------------
	@IntentHandler('getStationInfo')
	def getStationInfo(self, session: DialogSession):
			if self._stationInfo == _UNKNOWN_RADIO_STATION:
				langSlot = 'stationErrorInfo'
				langText = []
			else:
				langSlot = 'getStationInfo'
				langText = [self._stationCurrent, self._stationInfo]

			self.endDialog(session.sessionId, self.randomTalk(langSlot, langText))


	#TODO-----------------------------------------------
	@IntentHandler('playAtAdditionalRoom')
	def playAtAdditionalRoom(self, session: DialogSession):
			self.logDebug("playAtAdditionalRoom")

			playSite 	= None if 'Room' not in session.slots else session.slots['Room']

			if self._playing == True and playSite:
				stationVolume=self.RADIO_STATIONS[self._stationCurrent][RadioStation.VOLUME].strip()[:-1]

				# Vi bruger i øjeblikket ikke alle oplysningerne, men du kan annoncere.
				# self.publish(_MULTIROOM_PLAYER_PLAY, json.dumps({'url': stationUrl,
				#                                                             'radioStation': self.stationCurrent,
				#                                                             'stationName': stationName,
				#                                                              'playSite': playSite},
				# 																														 'stationVolume': stationVolume}))

				if playSite == 'base':
					playSite = self._baseServer

				self.publish(_MULTIROOM_PLAYER_PLAY, json.dumps({'playSite': playSite,  'stationVolume': stationVolume}))
				self.endDialog(session.sessionId, self.randomTalk('playAtAdditionalRoom', [playSite]))
			else:
				# No active radio station now.
				self._error(session.sessionId, 'stationErrorInfo')


	#TODO-----------------------------------------------
	@IntentHandler('stopPlayAt')
	def stopPlayAt(self, session: DialogSession):
		playSite 	= None if 'Room' not in session.slots else session.slotValue('Room').lower()

		if not playSite:
			self.endDialog(session.sessionId, self.randomTalk('errorSlotLocation'))
			return

		if playSite == 'base':
			playSite = self.baseServer

		self.mqttClient.publish(_MULTIROOM_PLAYER_STOP, json.dumps({'playSite': playSite}))

		self.endDialog(session.sessionId, self.randomTalk('stopPlayAt', [playSite]))


	#TODO------------------------------------------------
	@IntentHandler('moveStreamTo')
	def moveStreamTo(self, session: DialogSession):

		playSite 	= None if 'Room' not in session.slots else session.slotValue('Room').lower()

		if not playSite:
			self._error(session.sessionId, 'errorSlotLocation')
			return

		try:
			stationVolume = self.RADIO_STATIONS[self._stationCurrent][RadioStation.VOLUME].strip()[:-1]
		except KeyError as e:
			self._error(session.sessionId, f'stationErrorInfo - {e}')
			return

		if self._playing == True:
			if playSite == 'base':
				playSite = self._baseServer

			self.publish(_MULTIROOM_PLAYER_STOP, json.dumps({'playSite': 'everywhere'}))
			self.publish(_MULTIROOM_PLAYER_PLAY, json.dumps({'playSite': playSite, 'stationVolume': stationVolume}))

			langSlot = 'movePlayer'
		else:

			langSlot = 'stationErrorInfo'

		self.endDialog(session.sessionId, self.randomTalk(langSlot))


	#-----------------------------------------------
	def _error(self, sessionId: str, errSlot: str='errorSlotDefault'):
		self.endDialog(sessionId, self.randomTalk(errSlot))


	#-----------------------------------------------
	def _doStopSendNoise(self):
		# self.logDebug(f"Going into _stopSendNoise ")
		try:
			cmd = '/usr/bin/killall cat >/dev/null 2>&1'
			subprocess.call(cmd, shell=True)
		except Exception as e:
			self.logDebug(f"Exceptionas: {e} ")

		self._stop()
		self._sendingWhiteNoise_sendingNoise = False
		try:
			self.ConfigManager.updateSkillConfigurationFile('MultiRoomRadioManager', 'sendOutWhiteNoise', 'False')
		except Exception as e:
			raise e



	#-----------------------------------------------
	def _doSendWhiteNoise(self):
		# self.logDebug(f"Going into _doSendWhiteNoise ")

		mixerLevel4Noise = self.getConfig('mixerLevel4Noise')
		self._sendingWhiteNoise = True
		self.publish(_MULTIROOM_ENTRY_VOLUME, json.dumps({'activeSoundApp': self.name,'stationVolume': str(mixerLevel4Noise)}))
		self.publish(_MULTIROOM_PLAYER_PLAY, json.dumps({'siteId': 'WhiteNoise', 'playSite': 'everywhere'}))
		try:
			cmd = '`/bin/cat /dev/urandom > /dev/shm/snapfifo`  >/dev/null 2>&1 &'
			subprocess.call(cmd, shell=True)
		except Exception as e:
			self.logDebug(f"Exceptionas: {e} ")


	#-----------------------------------------------
	def setOutSendWhiteNoise(self, sendOutWhiteNoise :str) -> bool:
		self._sendOutWhiteNoise = sendOutWhiteNoise

		# self.logDebug(f"Going into setSendWhiteNoise - self._sendOutWhiteNoise: {self._sendOutWhiteNoise} ")
		if self._sendOutWhiteNoise:
			self._stop()
			self._doSendWhiteNoise()
		else:
			self._doStopSendNoise()

		return True


	#-----------------------------------------------
	def setDNDWhenStartPlaying(self, setDNDWhenStartPlaying :str) -> bool:
		self._setDNDWhenStartPlaying = setDNDWhenStartPlaying

		return True
