var express = require('express');
var router = express.Router();
var formidable = require('formidable');
var path = require('path');
var fs = require('fs');


router.post('/', function(req, res, next) {
  
  const form = formidable({multiples: true, uploadDir: path.dirname(__dirname) + "/uploads"});
  form.parse(req, (err, fields, files) => {
    if (err) {
      next(err);
      return;
    }
    for (f in files) {
      fs.rename(files[f].path, files[f].path + "_" + files[f].name, (error) => next(error));
    }
    res.json({success: true});
  }); 
});

module.exports = router;