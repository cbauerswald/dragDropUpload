var express = require('express');
var router = express.Router();
var formidable = require('formidable');
var path = require('path');
var fs = require('fs');

function renameFile(f, next) {
  fs.rename(f.path, f.path + "_" + f.name, (error) => next(error));
}

router.post('/', function(req, res, next) {
  
  //create a formidable object that will upload to our desired directory
  const form = formidable({multiples: true, uploadDir: path.dirname(__dirname) + "/uploads"});
  
  //parse out and sace the information contained in the request
  form.parse(req, (err, fields, files) => {
    if (err) {
      next(err);
      return;
    }
    for (key in files) {
      renameFile(files[key], next);
    }
    res.json({success: true});
  }); 
});

module.exports = router;