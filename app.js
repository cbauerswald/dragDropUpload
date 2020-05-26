var express = require('express');
var app = express();
var path = require('path');

//set up views
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

//routers
var indexRouter = require('./routes/indexRouter.js');
var uploadRouter = require('./routes/uploadRouter.js');

app.use('/', indexRouter);
app.use('/fileupload', uploadRouter);

app.listen(3000);