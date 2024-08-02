var http = require('http');
var url = require('url');
var mongodb = require('mongodb');
const {
  MONGO_URL,
  MONGO_DATABASE
} = process.env;

var MongoClient = mongodb.MongoClient;
var uri = mongodb://${MONGO_URL}/${MONGO_DATABASE};
var server = http.createServer(function (req, res) {
  var parsedUrl = url.parse(req.url, true);
  var student_id = parseInt(parsedUrl.query.student_id);
  if (/^\/api\/score/.test(req.url)) {
    MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true }, function(err, client) {
      if (err) throw err;
      var db = client.db("studentdb");
      db.collection("students").findOne({ "student_id": student_id }, (err, student) => {
        if (err) throw new Error(err.message, null);
        if (student) {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(student) + '\n');
        } else {
          res.writeHead(404);
          res.end("Student Not Found \n");
        }
      });
    });
  } else {
    res.writeHead(404);
    res.end("Wrong url, please try again\n");
  }
});
server.listen(8080);
