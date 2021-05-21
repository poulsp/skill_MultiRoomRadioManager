#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Program der opdaterer radio listen på radio player der kører på snips base server.
# Radio listen du laver ændringer i er radio_stations.csv, bare med en normal text editor.

# Program that updates the radio list on the radio player running on snips base server.
# The radio list you make changes to is radio_stations.csv, just with a normal text editor

import sys
sys.path.insert(0, './library')
# from socket import timeout
import urllib.request
import signal
def terminateProcess(signalNumber, frame):
	sys.exit()
signal.signal(signal.SIGTERM, terminateProcess)
signal.signal(signal.SIGINT, terminateProcess)


#import platform
import json
#import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
# import time

# import logging
# logging.basicConfig(
# 	#format='%(asctime)s {%(pathname)s:%(lineno)d - [%(levelname)s] - %(message)s',
# 	format='%(asctime)s - %(filename)s:%(lineno)d - [%(levelname)s] - %(message)s',
# 	level=logging.DEBUG,
# 	#level=logging.INFO,
# 	#level=logging.CRITICAL,
# )
# ,
# #   # filename='/var/log/test.log',
# #   # filemode='w'

from radioHelper import(RadioHelper,
# 												STATION_NAME,
# 												DESCRIPTION,
# 												VOLUME,
# 												STATION_URL,
# 												ONLINE,
# 												MAX_RADIO_LISTE_SIZE
)

#-----------------------------------------------
class ConfigurationError(Exception):
  pass

#_config = ""
global _config
#-----------------------------------------------
def readConfig():
	global _config
	with open('config.json') as config_file:
			_config = json.load(config_file)
#	print(f"##### _config: {_config}")
#	print(f"##### _config['aliceHost']: {_config['aliceHost']}")


#-----------------------------------------------
def getConfig(configName: str):
	global _config
	return _config[configName]


#-----------------------------------------------
if __name__ == '__main__':
	global _config
	DEBUG_HIDE = False

	readConfig()

	_aliceHost = getConfig('aliceHost')
	_aliceWebPort = getConfig('aliceWebPort')

	if getConfig('aliceHost') == "<aliceHostIp>":
		raise ConfigurationError('you must edit the config.json file.')

	if getConfig('aliceWebPort') == "<aliceWebPort>":
		raise ConfigurationError('you must edit the config.json file.')


	radioHelper = RadioHelper()
	if DEBUG_HIDE:
		pass
	else:
		radioHelper.printRadioliste()

	radioListJson = radioHelper.radioListJson
	radioList = radioHelper.getRadioStations()
	radioListToPublish = {'newRadioList':'jeps', 'radioList': radioList}

	_RADIO_UPDATE_RADIOSTATIONS = 'psp/multiroom/radio/update/radiostations'

	siteIsUp = False
	try:
		siteUrl  = urllib.request.urlopen(f"http://{_aliceHost}:{_aliceWebPort}", timeout=2)
		siteIsUp = siteUrl.getcode() == 200

	# except (urllib.error.HTTPError, urllib.error.URLError)  as e:
	except (urllib.error.HTTPError, urllib.error.URLError):
		siteIsUp = False

	if siteIsUp:
		print("Waiting, connecting with host.")
	else:
		print(f"Cannot connect to host, is ProjectAlice running? - aliceHost: {_aliceHost} - aliceWebPort: {_aliceWebPort}")
		sys.exit()

	try:
		publish.single(_RADIO_UPDATE_RADIOSTATIONS, radioListJson.encode('utf-8'), hostname=_aliceHost)
	except (OSError, ConnectionRefusedError):
		print(f"Connection refused til {_aliceHost}")

	print("Finish, Radio list updated.")
