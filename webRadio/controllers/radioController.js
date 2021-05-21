var async = require('async');

const getRadiolist  = require('../helpers/myHelper.js').getRadiolist
const send2Alice  = require('../helpers/myHelper.js').send2Alice

exports.index = function(req, res) {
  deviceUid = req.query.deviceUid
  deviceUidOrg = deviceUid

  if (deviceUid == undefined) { deviceUid = 'undefined' }

  async.waterfall([
   produce_radio_list
  ], function(err, results) {
      res.render('radios',  { page:'Radio Stations', menuId:'radio', title: 'Radio Stations', error: err, deviceUid, tableRowData: results });
    }
  )
}


//-----------------------------------------------
function produce_radio_list(callback) {
  // function (radioStations) is the callback
  getRadiolist(function (radioStations) {
    // process the async result.
    let radioStationList = []

    for(let radioStation in radioStations) {
      station = parseInt(radioStation.replace('radio ', ''))
      rest = radioStations[radioStation]

      if (station != 0) {
        radioStationList[station] = rest //tableRow
      }
    }

    let tableRows = []
    const desc   = 0
    const level  = 1
    const url    = 2
    const online = 3

    for(let station in radioStationList) {
      led = ""
      if (radioStationList[station][online] == true) {
        led = "led-green"
      }
      else {
        led = "led-red"
      }

      tableRow = `\
      <tr id="${station}"><td>${station}</td>\
      <td>${radioStationList[station][desc]}</td>\
      <td>&nbsp&nbsp&nbsp${radioStationList[station][level]}</td>\
      <td><button class="${led}"></button></td>\
      <td><a href="#" class="w3-bar-item w3-button w3-khaki w3-border border-blue w3-round w3-tiny" style="margin:2px; margin-left:10px" onclick="loadRadio('${station}/true/${deviceUid}')">Play</a></td>\
      </tr>\
      `

      if (station != 0) {
        tableRows[station] = tableRow
      }
    }

    callback(null, tableRows)
  })

  return
}
