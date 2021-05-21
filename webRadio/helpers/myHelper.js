var request = require('request');
const MQTT = require("async-mqtt");
const MQTT_SERVER_URL = `mqtt://${global.gConfig.aliceIp}:1883`
//const fetch = require('node-fetch');
//const FormData = require('form-data');

//-----------------------------------------------
const send2RadioManagerWidget = async (topic, payload) => {
  send2Alice(topic, payload)
}


//-----------------------------------------------
const send2Alice = async (topic, payload) => {
  let client = MQTT.connect(MQTT_SERVER_URL)
  try {
    await client.publish(topic, payload);
    // This line doesn't run until the server responds to the publish
    await client.end();
    // This line doesn't run until the client has disconnected without error
    //console.log("Done");
  } catch (e){
    // Do something about it!
    console.log(e.stack);
    process.exit();
  }
}


//-----------------------------------------------
function send2AliceApi(query, deviceUid, redirection, req, res, next) {

  let options = {
    'method': 'POST',
    'followAllRedirects': false,
    'url': `http://${global.gConfig.aliceIp}:${global.gConfig.apiPort}/api/v1.0.1/dialog/process/?=`,
    'headers': {
      'auth': global.gConfig.apiToken
    },
    formData: {
      'query': query
    }
  };

  let formDataWithDeviceUid = {
        'deviceUid': deviceUid
      }

  if (deviceUid != 'undefined') {
    Object.assign(options['formData'], formDataWithDeviceUid);
  }

  request(options, function (error, response) {
    if (error) throw new Error(error)
    res.redirect(redirection)
  })
}


//-----------------------------------------------
const getRadiolist = async (callback) => {
  let client = MQTT.connect(MQTT_SERVER_URL);
  let radioStations = Object

  try {
    await client.on("connect",
      function() {
        //_MULTIROOM_SEND_RADIO_RADIOSTATIONS
        client.subscribe('psp/multiroom/radio/send/radiostations')
      });
    await client.on('message', function (topic, payload) {
        // payload is Buffer
        radioStations = JSON.parse(payload).radioStations
        client.end()
      });
    await client.on('end', function () {

      callback(radioStations)
     })
    // _MULTIROOM_QUERY_RADIO_RADIOSTATIONS
    await client.publish('psp/multiroom/radio/query/radiolist', 'true')

  } catch (e){
    // Do something about it! if an error.
    console.log(e.stack)
    process.exit();
  }
}


module.exports = {send2Alice, send2AliceApi, MQTT, MQTT_SERVER_URL, getRadiolist, send2RadioManagerWidget }
