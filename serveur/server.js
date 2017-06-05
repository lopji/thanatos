var db = require('./database'),
        fs = require('fs');

function findByName(name) {
    var i;
    for (i = 0; i < this.computers.length; i++) {
        if (this.computers[i].name === name) {
            return i;
        }
    }
    return -1;
}

function available(element) {
    return element.connected === 1 && element.state === 0;
}

function id_project(id) {
    return function (element) {
        return element.id === id;
    };
}

function id_instance(id) {
    return function (element) {
        return element.project_id === id;
    };
}


function add(computer) {
    id = this.findByName(computer.name);
    if (id === -1) {
        this.computers.push(computer);
    } else {
        this.computers[id].connected = computer.connected;
        this.computers[id].status = computer.status;
        this.computers[id].error = computer.error;
        this.computers[id].state = computer.state;
    }
}

function launch(id, name, socket) {
    var parent = this;
    console.log("test1");
    db.constructor.query("SELECT instance.id, dataset, network, number, instance.title, project_id FROM instance join data on data_id = data.id join network on network_id = network.id where instance.id = ?", id)
            .on('result', function (instance) {
                console.log("test2");
                var id = parent.findByName(name);
                if (id !== -1) {
                    console.log("test3");
                    parent.computers[id].id = instance.id;
                    parent.computers[id].title = instance.title;
                    parent.computers[id].project_id = instance.project_id;
                    console.log(__dirname + '/uploads/saves/' + id + '.npz');
                    socket.emit("launch", {name: name, id: instance.id, network: instance.network, dataset: instance.dataset, number: instance.number, last: fs.existsSync(__dirname + '/uploads/saves/' + instance.id + '.npz')});
                }
            })
            .on('error', function (error) {
                 console.log("test4");
                console.log(error);
            });
}

var Server = (function () {
    var instance;

    function createInstance() {
        var object = new Object();
        object.computers = [];
        object.add = add;
        object.findByName = findByName;
        object.available = available;
        object.id_project = id_project;
        object.id_instance = id_instance;
        object.launch = launch;
        return object;
    }

    return {
        getInstance: function () {
            if (!instance) {
                instance = createInstance();
            }
            return instance;
        }
    };
})();

exports.constructor = Server;