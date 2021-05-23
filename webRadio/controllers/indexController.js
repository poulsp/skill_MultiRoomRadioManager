
exports.index = function(req, res, next) {
  res.render('index', {page:'Home', menuId:'home', 'radioUrl': 'http://192.168.3.16:4000/radios', 'volumeUrl': 'http://192.168.3.16:1780'})
};

