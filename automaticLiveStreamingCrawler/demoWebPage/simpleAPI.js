var url = require('url');
var http = require('http');
var fs = require('fs');
const express = require('express');
const app = express();
var cors = require('cors');
app.use(cors());

app.get('/', function(req, res){
	var params = url.parse(req.url, true).query;
	var dataFile = fs.readFileSync(params.platform+'.txt', {encoding: 'utf-8'})
	
	res.write(dataFile);
    res.end();
});

app.listen(3000, function(){
	console.log('Listening on port 3000...');
});