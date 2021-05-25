const express = require('express')
const router = express.Router()
const request = require('request')

const send2Alice  = require('../helpers/myHelper.js').send2Alice
const send2AliceApi  = require('../helpers/myHelper.js').send2AliceApi


//-----------------------------------------------
// Require controller modules.
const radio_controller = require('../controllers/radioController')


//-----------------------------------------------
// GET radios.
router.get('/radios', radio_controller.index)


//-----------------------------------------------
 // GET DND.
router.get('/radio/dnd', function(req, res, next) {
  send2Alice('psp/dnd', '')
  res.redirect('')
})


//-----------------------------------------------
// GET DND.
router.get('/radio/cancel_dnd', function(req, res, next) {
  send2Alice('psp/cancelDnd', '')
  res.redirect('')
})


//-----------------------------------------------
// GET speaker On.
router.get('/radio/speakerOn/:deviceUid', function(req, res, next) {
  send2AliceApi('speaker on', req.params['deviceUid'], '', req, res, next)
})


//-----------------------------------------------
// GET speaker Off.
router.get('/radio/speakerOff/:deviceUid', function(req, res, next) {
  send2AliceApi('speaker off', req.params['deviceUid'], '', req, res, next)
})


//-----------------------------------------------
// GET speaker On.
router.get('/radio/mute/:deviceUid', function(req, res, next) {
  send2AliceApi('mute', req.params['deviceUid'], '', req, res, next)
})


//-----------------------------------------------
// GET speaker Off.
router.get('/radio/unmute/:deviceUid', function(req, res, next) {
  send2AliceApi('unmute', req.params['deviceUid'], '', req, res, next)
})


//-----------------------------------------------
// GET Volume up.
router.get('/radio/volumeUp', function(req, res, next) {
  // _MULTIROOM_GESTURE_SENSOR_VOLUME_UP   = "psp/multiroom/sensor/gesture/volumeUp"
  send2Alice('psp/multiroom/sensor/gesture/volumeUp', 'dummy')
  res.redirect('')
})


//-----------------------------------------------
// GET Volume Down.
router.get('/radio/volumeDown', function(req, res, next) {
  //_MULTIROOM_GESTURE_SENSOR_VOLUME_DOWN = "psp/multiroom/sensor/gesture/volumeDown"
  send2Alice('psp/multiroom/sensor/gesture/volumeDown', 'dummy')
  res.redirect('')
})


//-----------------------------------------------
// GET Stop playing.
router.get('/radio/stop/:deviceUid', function(req, res, next) {
  send2AliceApi('stop radio', req.params['deviceUid'], 'stop', req, res, next)
})

//-----------------------------------------------
 // GET Play a radiostation.
router.get('/radio/:station/:everywhere/:deviceUid', function(req, res, next) {
  const station = req.params['station']
  const everywhere = req.params['everywhere']

  let query = ''

  if (everywhere === "true") {
    query = `play radio ${station} at everywhere`
  }
  else
    query = `play radio ${station}`
  console.log(`station: ${station}`)
  //send2AliceApi(query, req.params['deviceUid'], '', req, res, next)
	send2AliceApi(query, req.params['deviceUid'], `${station}`, req, res, next)
})


module.exports = router
