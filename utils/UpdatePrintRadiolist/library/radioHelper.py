import logging
import csv
import json

STATION_NAME = 0
DESCRIPTION  = 1
VOLUME       = 2
STATION_URL  = 3
ONLINE       = 4

MAX_RADIO_LISTE_SIZE = 170

class RadioHelper(object):
	def __init__(self):
		super(RadioHelper, self).__init__()

		#logging.debug("in class RadioHelper")

		self.MAX_radio_liste_size = MAX_RADIO_LISTE_SIZE
		self.radio_liste = [''] * self.MAX_radio_liste_size

		#self.RADIO_STATIONS = {'skillDist': 'RadioManager', 'stations': {}}
		self.RADIO_STATIONS = {}

		self.getRadioListCsv()
		self._radioListJson = json.dumps(self.getRadioStations())


	#-----------------------------------------------
	def getRadioStations(self):
		return self.RADIO_STATIONS


	#-----------------------------------------------
	@property
	def radioListJson(self):
		#print(f"self.getRadioStations(): {self.getRadioStations()}")

		return self._radioListJson


	#-----------------------------------------------
	def getRadioListCsv(self):
		"""get/read_radio_liste_csv(self)"""
		file_name = "./radio_stations.csv"
		#logging.debug("getRadioListCsv")
		# read radio_stations_as csv_file and insert in RADIO_STATIONS.
		with open('radio_stations.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
					print()
					#print(f'Column names are {", ".join(row)}')
					line_count += 1
				else:
					if row[0][0] != "#":
						self.RADIO_STATIONS[row[STATION_NAME]] = [(row[DESCRIPTION].strip()), row[VOLUME].strip() + "%", row[STATION_URL].strip(), row[ONLINE].strip() == 'True']
						line_count += 1


	#-----------------------------------------------
	def getRadioList(self):
		for i in self.getRadioStations().keys():
			station_no = int(i[5::])
			self.radio_liste[station_no] = i

		return self.radio_liste


	#-----------------------------------------------
	def linjeskift(self):
		print()


	#-----------------------------------------------
	def udskriv(self, x):
		station_name1 = ""
		station_name2 = ""
		description1 = ""
		description2 = ""

		if self.radio_liste[x] != '':
			station_name1 = self.radio_liste[x]
			description1 = self.radio_stations[station_name1][0]


		if self.radio_liste[x+10] != '':
			station_name2 = "| " + self.radio_liste[x+10]
			description2 = self.radio_stations[self.radio_liste[x+10]][0]
		else:
			station_name2 = "|"

		print("{:9s} {:36s} {:9s} {:31s}".format(station_name1,description1, station_name2, description2))


	#-----------------------------------------------
	def printRadioliste(self):
		self.radio_stations = self.getRadioStations()

		self.radio_liste = self.getRadioList()

		for x in list(range(10)):
			self.udskriv(x)
		self.linjeskift()
		for x in list(range(20,30)):
			self.udskriv(x)
		self.linjeskift()
		for x in list(range(40,50)):
			self.udskriv(x)
		self.linjeskift()
		for x in list(range(60,70)):
			self.udskriv(x)
		self.linjeskift()
		for x in list(range(80,90)):
			self.udskriv(x)
		self.linjeskift()
		for x in list(range(100,110)):
			self.udskriv(x)
		self.linjeskift()

