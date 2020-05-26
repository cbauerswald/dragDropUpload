var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next) {
	res.render('index', {"name": "Cecelia"});
});

module.exports = router;