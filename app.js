const express = require('express');
const app = express();
const path = require('path');
const fs = require('fs');


//set up views
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

//set up static directory
app.use(express.static('public'));

//routers
var indexRouter = require('./routes/indexRouter.js');
var uploadRouter = require('./routes/uploadRouter.js');

app.use('/', indexRouter);
app.use('/fileupload', uploadRouter);

//create directory for uploads if it doesn't already exist
var dir = './uploads';

if (!fs.existsSync(dir)){
    fs.mkdirSync(dir);
}

console.log('Server is listening on port 5000')
app.listen(5000);
