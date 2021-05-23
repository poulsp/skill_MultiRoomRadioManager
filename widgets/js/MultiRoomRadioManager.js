class MultiRoomRadioManager_MultiRoomRadioManager extends Widget {

	//-----------------------------------------------
	constructor(uid, widgetId) {
		super(uid, widgetId);
		this.widgetId = widgetId
		this.uid = uid
		this.deviceUid = localStorage.getItem('interfaceUid')
		this.aliceSettings = JSON.parse(window.sessionStorage.aliceSettings);
		//console.log(`################ this.aliceSettings: ${Object.keys(this.aliceSettings)}`)

		this.myIframe = document.querySelector(`[data-ref="MultiRoomRadioManager_radio_${this.uid}"]`)
		this.myExplanationDiv = document.querySelector(`[data-ref="MultiRoomRadioManager_explanation_${this.uid}"]`)
		this.smileyImg = document.querySelector(`[data-ref="MultiRoomRadioManager_smiley_img_${this.uid}"]`)
		this.myImg = document.querySelector(`[data-ref="MultiRoomRadioManager_img_${this.uid}"]`)
		this.getBaseData()

		this.subscribe('psp/radiomanager/widget/refresh', this.getBaseData)
	}


	//-----------------------------------------------
	getBaseData() {

			fetch(`http://${this.aliceSettings['aliceIp']}:${this.aliceSettings['apiPort']}/api/v1.0.1/widgets/${this.widgetId}/function/baseData/`, {
			method: "POST",
			body: '{}',
			headers: {
				'auth': localStorage.getItem('apiToken'),
				'content-type': 'application/json'
			}
			})
			.then((res) => res.json())
			.then((data) => {
				this.webRadioManagerPort 	= data.data.webRadioManagerPort
				this.siteIsUp		          = data.data.siteIsUp
			})
			.then(() => this.checkRadioWidgetDisplay())
	}


	//-----------------------------------------------
	checkRadioWidgetDisplay() {
		if (this.siteIsUp) {
			this.myExplanationDiv.style.display = "none";
			this.smileyImg.display = "none";
			this.myImg.style.display = "none";
			this.myIframe.style.display = "block";

			this.showSiteRadioTable()
		}
		else {
			this.myIframe.style.display = "none";
			this.smileyImg.src = `http://${window.location.hostname}:5001/api/v1.0.1/widgets/resources/img/MultiRoomRadioManager/smiley.png`
			this.myImg.src = `http://${window.location.hostname}:5001/api/v1.0.1/widgets/resources/img/MultiRoomRadioManager/MultiRoomRadioManagerWidget.png`
			this.smileyImg.display = "block";
			this.myImg.style.display = "block";
			this.myExplanationDiv.style.display = "block";
		}
	}


	//-----------------------------------------------
	showSiteRadioTable() {
		this.myIframe.src = `http://${this.aliceSettings['aliceIp']}:${this.webRadioManagerPort}/radios?deviceUid=${this.deviceUid}`
	}

}
