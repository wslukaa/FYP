var http = require('http');
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";
var fs = require('fs');
var express = require('express');
var app = express();
/*
MongoClient.connect(url, function(err, db) {
	if(err) throw err;
	console.log("Database connected");
	var dbo = db.db("fyp");
	var query = { ht_name: "#momlife"};
	dbo.collection("ht").find(query).toArray(function(err, result) {
		if (err) throw err;
		console.log(result);
		db.close();
	});
});*/

http.createServer(function (req, res) {
	fs.readFile('learning.html', function(err, data) {
		res.writeHead(200, {'Content-Type': 'text/html'});
		res.write(data);
		res.end();
	})
}).listen(8080);