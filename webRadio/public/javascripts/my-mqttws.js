//-----------------------------------------------
function startMqtt() {

	myMqtt = new MyMqtt();
}


// ############# Mqtt part #############
// /object.addEventListener("load", startConnect());
class MyMqtt {
  constructor() {
		this.radioServerDownDiv = document.querySelector('.RadioServerDown')
		this.floatContainerDiv = document.querySelector('.float-container')
		this.iFrameRadiolist = document.querySelector('.frame-radio')
	  this.startConnect()
  }


	startConnect() {
		// Generate a random client ID
		let clientId = "clientId-" + parseInt(Math.random() * 100);

	// Lav et alice api call
		let host = window.location.hostname //"localhost"
		let port = "1884"

		// Initialize new Paho client connection
		this.client = new Paho.MQTT.Client(host, Number(port), clientId);

		// Set callback handlers
		this.client.onConnectionLost = this.onConnectionLost.bind(this);
		this.client.onMessageArrived = this.onMessageArrived.bind(this);

		// Connect the client, if successful, call onConnect function
		this.client.connect({onSuccess:this.onConnect.bind(this)});
		// or, surprisingly for you, by removing all this. in front of client and message references.
	}

	// Called when the client connects
	onConnect() {
		// Subscribe to the requested topic
		this.client.subscribe('psp/radiomanager/widget/refresh');
	}

	// Called when the client loses its connection
	onConnectionLost(responseObject) {
		if (responseObject.errorCode !== 0) {
			console.warn(`responseObject.errorCode: ${responseObject.errorMessage}`)
		}
	}

	// Called when a message arrives
	onMessageArrived(message) {

		if (message.destinationName == 'psp/radiomanager/widget/refresh') {
			if (message.payloadString == 'dummy') {
				this.radioServerDownDiv.style.display = "none";
				this.floatContainerDiv.style.display = "block";
				this.iFrameRadiolist.contentDocument.location.reload(true);
			}
			else if (message.payloadString == 'WebRadioStart') {
				this.radioServerDownDiv.style.display = "none";
				this.floatContainerDiv.style.display = "block";
			}

			else if (message.payloadString == 'WebRadioStop') {
				this.radioServerDownDiv.style.display = "block";
				this.floatContainerDiv.style.display  = "none";
			}

		}
	}

	// Called when the disconnection button is pressed
	disconnect() {
		this.client.disconnect();
	}
}
