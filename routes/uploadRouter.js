var express = require('express');
var router = express.Router();
var formidable = require('formidable');
var path = require('path');

router.post('/', function(req, res, next) {

  const form = formidable({multiples: true, uploadDir: path.dirname(__dirname) + "/uploads"});
  form.parse(req, (err, fields, files) => {
    if (err) {
      next(err);
      return;
    }
    res.json({fields, files});
  }); 
});

module.exports = router;