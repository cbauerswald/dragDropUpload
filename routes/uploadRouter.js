var express = require('express');
var router = express.Router();
var formidable = require('formidable');
var path = require('path');
var fs = require('fs');
const {spawn} = require('child_process');

function renameFile(f, next) {
  fs.rename(f.path, f.path + "_" + f.name, (error) => next(error));
}

function parseFiles(files) {
    // Spawn new child process to call the python script
    // Send files object as string to python parser script.
    const python = spawn('python', ['parser.py', JSON.stringify(files)]);

    // Ensure python process is finished (gives code 0 if success).
    python.on('close', (code) => {
      console.log(`child process close all stdio with code ${code}`);
    })
}

router.post('/', function(req, res, next) {
  
  //create a formidable object that will upload to our desired directory
  const form = formidable({multiples: true, uploadDir: path.dirname(__dirname) + "/uploads"});
  
  //parse out and save the information contained in the request
  form.parse(req, (err, fields, files) => {
    if (err) {
      next(err);
      return;
    }

    var numFiles = 0; 
    //files[0] is either a single file or an array containing all uploaded files
    if (files["files[]"].length > 0) {
      numFiles = files["files[]"].length;
      //if there are multiple files
      for (i in files["files[]"]) {
        renameFile(files["files[]"][i], next);
      }
    } else {
      numFiles = 1;
      //if there is only one file
      renameFile(files["files[]"], next);
    }

    // Launches python script.
    parseFiles(files);

    res.json({success: true, fileCount: numFiles});
  }); 
});

module.exports = router;