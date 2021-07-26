from os import path
import json
import subprocess

# from core.util.model.Logger import Logger



class WebRadioManager():
	_exportCmd = 'export NVM_DIR="$HOME/.nvm";[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh";[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"'


	#-----------------------------------------------
	def __init__(self, parent, aliceIp, webRadioManagerPort='4000', aliceWebInterfacePort='5000', apiPort='5001', apiToken='unknown'):
		super().__init__()

		self._config = {}

		self.parent 								= parent
		self._aliceIp 							=	aliceIp
		self._aliceWebInterfacePort	= aliceWebInterfacePort
		self._apiPort								= apiPort
		self._nodePort							= webRadioManagerPort
		self._apiToken							= apiToken

		self._CanStartServer = False


	#-----------------------------------------------
	def checkConfig(self):
		# check the properties and possibly. put in the right properties.
		self._readConfig()

		nodePort = self._config['development']['node_port']
		aliceIp = self._config['development']['aliceIp']
		aliceWebInterfacePort = self._config['development']['aliceWebInterfacePort']
		apiPort = self._config['development']['apiPort']
		apiToken = self._config['development']['apiToken']

		changes = False
		if nodePort != self._nodePort:
			self._config['development']['node_port'] = self._nodePort
			changes = True

		if aliceIp != self._aliceIp:
			if aliceIp != 'Unknown': # or check validity
				self._config['development']['aliceIp'] = self._aliceIp
				changes = True

		if aliceWebInterfacePort != self._aliceWebInterfacePort:
			self._config['development']['aliceWebInterfacePort'] = self._aliceWebInterfacePort
			changes = True

		if apiPort != self._apiPort:
			self._config['development']['apiPort'] = self._apiPort
			changes = True

		if apiToken != self._apiToken:
			if self._apiToken != 'unknown': # or check validity
				self._config['development']['apiToken'] = self._apiToken
				changes = True

		if changes:
			self._writeConfig()

		if aliceIp == 'Unknown':
			self._CanStartServer = False
		else:
			self._CanStartServer = True

		if self._apiToken == 'unknown': # or check validity
			self._CanStartServer = False
		else:
			self._CanStartServer = True


	#-----------------------------------------------
	def _readConfig(self):
		if not path.exists('./skills/MultiRoomRadioManager/webRadio/config/config.json'):
			cmd = "cp ./skills/MultiRoomRadioManager/webRadio/config/config.json.sample ./skills/MultiRoomRadioManager/webRadio/config/config.json"
			subprocess.call(cmd, shell=True)

		with open("./skills/MultiRoomRadioManager/webRadio/config/config.json", "r") as read_file:
			data = json.load(read_file)

		self._config = data


	#-----------------------------------------------
	def _writeConfig(self):
		with open('./skills/MultiRoomRadioManager/webRadio/config/config.json', 'w') as json_file:
			json.dump(self._config, json_file, sort_keys=True, indent=4 )


	#-----------------------------------------------
	def startWebserver(self):
		if self._CanStartServer:
			try:
					# "whoami",
					# "nvm current",
					# "/usr/bin/which node",
				node = subprocess.check_output(
					f"{WebRadioManager._exportCmd} && /usr/bin/which node",
					stderr=subprocess.STDOUT,
					shell=True
				).decode('utf-8').replace('\n','')

			except subprocess.CalledProcessError:
			# except subprocess.CalledProcessError as e:
				# Logger().logInfo(f"########################################## line 112 except: {e}")
				cmd =f"cd ~/ProjectAlice/skills/MultiRoomRadioManager/webRadio/MyExtra  && {WebRadioManager._exportCmd} && ./webRadio-start.sh > /dev/null 2>&1 &"
				return

			node = node[3:] #nvm/home/pi/.nvm/versions/node/v12.18.4/bin/node
			cmd =f"{node} ~/ProjectAlice/skills/MultiRoomRadioManager/webRadio/bin/www > /dev/null 2>&1 &"

			subprocess.call(cmd, shell=True)

	#-----------------------------------------------
	def stopWebserver(self):
		pass
		# cmd = f"cd ~/ProjectAlice/skills/MultiRoomRadioManager/webRadio/MyExtra && {WebRadioManager._exportCmd} && ./webRadio-stop.sh > /dev/null 2>&1 &"
		# subprocess.call(cmd, shell=True)

