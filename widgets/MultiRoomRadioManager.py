import sqlite3
import requests
import urllib.request
import json

from core.webui.model.Widget import Widget
from core.webui.model.WidgetSizes import WidgetSizes


class MultiRoomRadioManager(Widget):

	# w_extralarge_wide: 700x500

	#DEFAULT_SIZE = WidgetSizes.w_small_wide
	DEFAULT_SIZE = WidgetSizes.w_extralarge_wide
	DEFAULT_OPTIONS: dict = dict()

	def __init__(self, data: sqlite3.Row):
		super().__init__(data)

		if self.settings:
			self.settings['title'] = False
			self.settings['borders'] = False
			self.w = 650
			self.h = 452

			# self.w = 700
			# self.h = 468


	#-----------------------------------------------
	def baseData(self) -> dict:
		webRadioManagerPort = self.skillInstance.getConfig('webRadioManagerPort')

		siteIsUp = False
		try:
			webUrl  = urllib.request.urlopen(f"http://{self._getAliceIp()}:{webRadioManagerPort}/radios")

			siteIsUp = webUrl.getcode() == 200
		# except Exception as e:
		except Exception:
			siteIsUp = False


		return {
			'webRadioManagerPort': webRadioManagerPort,
			'siteIsUp': siteIsUp
		}


	#-----------------------------------------------
	def _getAliceIp(self):

		url = 'http://localhost:5001/api/v1.0.1/utils/config/'
		headers = {
		  "auth": "SECRET_TOKEN"
		}

		response = requests.request('GET', url, headers=headers)
		aliceIp = json.loads(response.text)['config']['aliceIp']

		return aliceIp
