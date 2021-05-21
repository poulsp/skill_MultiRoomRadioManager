var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

/*
process.env.NODE_ENV = 'development';

// uncomment below line to test this code against staging environment
//process.env.NODE_ENV = 'production';

// config variables
const config = require('./config/config.js');
*/

var radioRouter = require('./routes/radio');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
// set path for static assets
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', radioRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

//_RADIOMANAGER_WIDGET_REFRESH = 'psp/radiomanager/widget/refresh'
require('./helpers/myHelper.js').send2RadioManagerWidget('psp/radiomanager/widget/refresh', 'start external webserver ')


module.exports = app;

/*
app.listen(global.gConfig.node_port, () => {
    console.log(`${global.gConfig.app_name} listening on port ${global.gConfig.node_port}`);
});
*/
