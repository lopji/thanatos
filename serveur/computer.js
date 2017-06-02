exports.constructor = function (name, connected, status, error, state) {
    this.name = String(name);
    this.connected = connected;
    this.status = status;
    this.error = error;
    this.state = state;
    this.id_project = -1;
    this.title = "";
};