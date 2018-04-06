var http = require('http');
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";
var fs = require('fs');
var express = require('express');
var app = express();
var query;



//var query = { ht_name: "#momlife"};

//the home page, which is not used
app.get('/', function(req, res) {
	fs.readFile('learning.html', function(err, data) {
		res.writeHead(200, {'Content-Type': 'text/html'});
		//res.write(data);
		res.write("Go to /search for searching, this page is reserved")
		res.end();
	})
})

//the page for search
app.get('/search', function(req, res) {
	fs.readFile('search.html', function(err, data) {
		res.writeHead(200, {'Content-Type': 'text/html'});
		res.write(data);
		res.end();
	})
})

app.get('/search/result',function(req, res) {
	//get the keywords from the query
	if (req.query.ts_start == "") {
		query = {
			ht_name: req.query.ht_name
		}
		console.log("ts_start is null")
	}	else {
		query = {
			ht_name: req.query.ht_name,
			ts_start: req.query.ts_start
		}
		console.log("the query has 2 parts")
	};
	

	//connet to Mongodb and get the data
	//The documents have to be inserted to MongoDb first
	MongoClient.connect(url, function(err, db) {
	if(err) throw err;
	console.log("Database connected");
	var dbo = db.db("fyp");
	//var query = { ht_name: "#momlife"};
	dbo.collection("ht").find(query).toArray(function(err, result) {
		if (err) throw err;
		console.log("%d object found, the coresponding json has been returned", result.length);
		res.send(result);
		db.close();
	});
});



})

//setup the localhost to port 8080
var server = app.listen(8080, function() {

	//var host = server.address().address
	var port = server.address().port

	console.log("You are hosting at localhost:%s", port)
})


