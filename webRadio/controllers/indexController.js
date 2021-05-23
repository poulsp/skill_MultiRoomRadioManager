
exports.index = function(req, res, next) {
	res.render('index', {page:'Home', menuId:'home', 'radioUrl': `http://${global.gConfig.aliceIp}:4000/radios`, 'volumeUrl': `http://${global.gConfig.aliceIp}:1780`})
};

