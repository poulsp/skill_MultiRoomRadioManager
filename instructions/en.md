# MultiRoomRadioManager


Manage internet radio stations and players in the synchronous multiroom audio system.

This skill requires and depends on the skill [MultiRoomMediaVolume](https://github.com/poulsp/skill_MultiRoomMediaVolume).
You also need the standalone [PspMultiRoomPlayer](https://github.com/poulsp/PspMultiRoomPlayer).
But you can test if the system work with the built-in web player in the MultiRoomMediaVolume widget, without the PspMultiRoomPlayer running.


You can create a widget in menupoint "WIDGET" with where you can list/play/stop stations.


![alt text](https://github.com/poulsp/skill_MultiRoomRadioManager/blob/master/widgets/img/MultiRoomRadioManagerWidget.png?raw=true)

You play a radio station with voice by saying e.g "radio 14" and the responses from alice "Tuning in to radio 14, 1.FM - Blues." and stop it by saying  "stop radio".

##### Controlling the volume by voice
	"volume up"
	"increase volume"
	"volume up 5"
	"increase volume by 5", "volume up at office 5 percent"
	same "volume down", "decrease volume"
	"get volume" "tell me the volume", "get volume at kitchen"

	"volume 11"
	"set the volume to 46 at kitchen"
	"mute", "mute volume", "volume mute", "volume mute at office",
	"unmute", "unmute volume", "volume unmute", "volume unmute at bedroom",


##### Other voice commands
	"tell me the station playing", "what station playing", "who is playing"
	"radio 11", "radio 37 at everywhere", "radio 23 at dining room", "play radio station 45"


##### Play at additional Rooms:
	"play at outdoor", "play at kitchen"


##### Moving stream:
	"move to lounge", "move to office"


In the skills folder ~/ProjectAlice/skills/MultiRoomRadioManager there is a folder utils/UpdatePrintRadiolist, in there we have a standalone app  UpdatePrintRadiolist.py and a file called radio_stations.csv.

To make changes in the radio list stations you add/change them in file 'radio_stations.csv', just with a normal text editor.
First run ./setup.sh, to create the virtual python environment.
Then run ./update_print_radioliste.py and the radio stations is updated on the fly in Alice.

This folder can be copied to another location if preferred.


You can test by download to alice skill folder.

cd ~/ProjectAlice/skills

git clone https://github.com/poulsp/skill_MultiRoomMediaVolume MultiRoomMediaVolume

git clone https://github.com/poulsp/skill_MultiRoomRadioManager MultiRoomRadioManager


Use the [PspMultiRoomPlayer](https://github.com/poulsp/PspMultiRoomPlayer) to play the actual sound/music
You can also control the volume of all devices and listen to radio / music outside (eg via bluetooth) with the Android app [snapcast] (https://play.google.com/store/apps/details?id=de. badaix snapcast)
