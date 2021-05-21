import platform
from os import path
import subprocess

_PLATFORM_MACHINE  = platform.machine()


class CheckNodejs():
	_nodeVersion = "v12.22.1"

	_exportCmd = 'export NVM_DIR="$HOME/.nvm";[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh";[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"'


	@staticmethod
	def test4Nodejs():
		retValue = False
		try:
			subprocess.check_output(
				"node -v",
				stderr=subprocess.STDOUT,
				shell=True
			).decode('utf-8').replace('\n','')
			retValue = True
		except subprocess.CalledProcessError:
			# No sucesss, try again
			try:
				cmd = CheckNodejs._exportCmd  + ';node -v'

				subprocess.check_output(
					cmd,
					stderr=subprocess.STDOUT,
					shell=True
				).decode('utf-8').replace('\n','')
				retValue = True

			except subprocess.CalledProcessError:
				# Install Nodejs via nvm.
				retValue = False

		return retValue


	#-----------------------------------------------
	@staticmethod
	def installNodejs():
		if _PLATFORM_MACHINE == "x86_64":
			cmd = "tar -xf ./skills/MultiRoomRadioManager/system/nvm-amd.tar -C ~/"
		elif _PLATFORM_MACHINE == "armv7l":
			cmd = "tar -xf ./skills/MultiRoomRadioManager/system/nvm-arm.tar -C ~/"

		subprocess.call(cmd, shell=True)

		cmd = f"cd && echo '{CheckNodejs._exportCmd}' >> .bashrc"
		subprocess.call(cmd, shell=True)

		try:
			path2Node = (subprocess.check_output(
			  f"{CheckNodejs._exportCmd} && which node",
			  stderr=subprocess.STDOUT,
			  shell=True
			).decode('utf-8').replace('\n',''))
			# it's okay
			pass
		except subprocess.CalledProcessError:
			pass

		path2Node = path2Node.replace('nvm/home', '/home')
		path2Node = path2Node.replace('/bin/node', '/bin')
		subprocess.call(f'sudo ln -s {path2Node}/node /usr/bin/node', shell=True)
		subprocess.call(f'sudo ln -s {path2Node}/nodejs /usr/bin/nodejs', shell=True)
		subprocess.call(f'sudo ln -s {path2Node}/npm /usr/bin/npm', shell=True)
		subprocess.call(f'sudo ln -s {path2Node}/npx /usr/bin/npx', shell=True)


	#-----------------------------------------------
	@staticmethod
	def checkNodeModules(parent):
		if not path.exists('./skills/MultiRoomRadioManager/webRadio/node_modules'):
			parent.logInfo(f'Checking dependencies **{parent.NAME}**, can take a little time, here by first install.')

			subprocess.call("cd ./skills/MultiRoomRadioManager/webRadio && npm install > /dev/null 2>&1", shell=True)


	#-----------------------------------------------
	@staticmethod
	def removeNodejs():
		pass
		# mv to .nvm_redady_2_be_deleted_if_you_wish_that  instead of remove it.
		# print("################################################### Er i removeNodejs")
		# cmd = "cd; rm -rf .nvm"
		# subprocess.call(cmd, shell=True)

		# Fjern fra .bashrc. med sed ???, hvorfor egentlig, den er harmløs

