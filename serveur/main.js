var express = require('express'),
        app = express(),
        messages = require('./langues/fr.json'),
        db = require('./database'),
        c = require('./computer'),
        srv = require('./server'),
        server = require('http').createServer(app),
        io = require('socket.io').listen(server),
        fs = require('fs'),
        path = require('path'),
        mime = require('mime'),
        multer = require('multer');

var upload = multer({dest: __dirname + '/tmp/'});

app.get('/networks', function (req, res) {
    console.log("REST networks");
    var array = {};
    fs.readdirSync(__dirname + '/uploads/networks').forEach(
            function (file) {
                array[file] = file;
            });
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify(array));
});

app.get('/datasets', function (req, res) {
    console.log("REST datasets");
    var array = {};
    fs.readdirSync(__dirname + '/uploads/datasets').forEach(function (file) {
        array[file] = file;
    });
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify(array));
});

app.get('/datasets/:dataset/:number', function (req, res) {
    console.log("REST download dataset");
    var dataset = req.params.dataset;
    var number = req.params.number;
    var file = __dirname + '/uploads/datasets/' + dataset + '/' + number;

    if (fs.existsSync(file)) {
        var filename = path.basename(file);
        var mimetype = mime.lookup(file);

        res.setHeader('Content-disposition', 'attachment; filename=' + filename);
        res.setHeader('Content-type', mimetype);

        var filestream = fs.createReadStream(file);
        filestream.pipe(res);
    }
});

app.get('/networks/:network', function (req, res) {
    console.log("REST download network");
    var network = req.params.network;
    var file = __dirname + '/uploads/networks/' + network;

    if (fs.existsSync(file)) {
        var filename = path.basename(file);
        var mimetype = mime.lookup(file);

        res.setHeader('Content-disposition', 'attachment; filename=' + filename);
        res.setHeader('Content-type', mimetype);

        var filestream = fs.createReadStream(file);
        filestream.pipe(res);
    }
});

app.get('/saves/get/:id', function (req, res) {
    console.log("REST download save");
    var id = req.params.id;
    var file = __dirname + '/uploads/saves/' + id;

    if (fs.existsSync(file)) {
        var filename = path.basename(file);
        var mimetype = mime.lookup(file);

        res.setHeader('Content-disposition', 'attachment; filename=' + filename);
        res.setHeader('Content-type', mimetype);

        var filestream = fs.createReadStream(file);
        filestream.pipe(res);
    }
});

app.post('/saves/post/:id', upload.any(), function (req, res) {
    console.log("REST upload file");
    if (fs.existsSync(__dirname + '/tmp/' + req.files[0].filename)) {
        var id = req.params.id;
        var source = fs.createReadStream(__dirname + '/tmp/' + req.files[0].filename);
        var dest = fs.createWriteStream(__dirname + '/uploads/saves/' + id + '.npz');
        source.pipe(dest);
        fs.unlinkSync(__dirname + '/tmp/' + req.files[0].filename);
    }
    res.send(200);
});

var s = srv.constructor.getInstance();

var javascript = io.of("/javascript");
var python = io.of("/python");
var php = io.of("/php");

javascript.on('connection', function (socket) {
    console.log('Client javascript connect');
    socket.emit("computers", s.computers);

    socket.on('start', function (array) {
        console.log("Client javascript on start");
        s.launch(array["id"], array["name"], python);
    });

    socket.on('resume', function (array) {
        console.log("Client javascript on resume");
        python.emit('resume', array);
    });

    socket.on('break', function (array) {
        console.log("Client javascript on break");
        python.emit('break', array);
    });

    socket.on('stop', function (array) {
        console.log("Client javascript on stop");
        python.emit('stop', array);
    });

    socket.on('save', function (array) {
        console.log("Client javascript on save");
        python.emit('save', array);
    });
});

python.on('connection', function (socket) {
    console.log('Client python connect');

    socket.on('validation', function (array) {
        console.log("Client python on validation");
        var id = s.findByName(String(array["name"]));
        if (id !== -1) {
            db.constructor.query("INSERT into `validation` set ?", {validation: array["validation"], training: array["training"], epoch: array["epoch"], accuracy: array["accuracy"], instance_id: s.computers[id].id})
                    .on('error', function (error) {
                        console.log(error);
                    });
            javascript.emit("validation", {validation: array["validation"], training: array["training"], epoch: array["epoch"], accuracy: array["accuracy"], instance_id: s.computers[id].id});
        }
    });

    socket.on('data', function (array) {
        console.log("Client python on data");
        s.add(new c.constructor(array["name"], 1, messages["status"][array["status"]], messages["error"][array["error"]], array["state"]));
        socket.name = array["name"];
        javascript.emit("computers", s.computers);
    });

    socket.on('disconnect', function () {
        console.log("Client python on disconnect");
        var id = s.findByName(socket.name);
        if (id !== -1) {
            s.computers[id].connected = 0;
            javascript.emit("computers", s.computers);
        }
    });
});

php.on('connection', function (socket) {
    console.log('Client php connect');

    socket.on('available', function () {
        console.log("Client php on available");
        var available = s.computers.filter(s.available);
        socket.emit('available', available);
    });

    socket.on('launch', function (array) {
        console.log("Client php on launch");
        s.launch(array["id"], array["name"], python);
    });
});

console.log("Start server on 8080");
server.listen(8080);