var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);

var redis = require('socket.io/node_modules/redis');
var client = redis.createClient();

io.sockets.on('connection', function (socket) {

    socket.on('rate_message', function (message) {
        console.log(123);
        console.log(message);
        client.get(message.DBID, function(err, res){
            console.log(res);
            var msgToDOM = {change: message.changed, title: message.title, projID: message.projID};
            io.sockets.socket(res).emit('show_in_dom_rate', msgToDOM);
        });



    });

    socket.on('comment_message', function(message){
        client.get(message.DBID, function(err, res){
            var msgToDOM = {firstName: message.FN, lastName: message.LN, title:message.title, ID: message.PID,
                            isPost: message.isPost};
            io.sockets.socket(res).emit('show_in_dom_comment', msgToDOM);
        });
    });

    socket.on('checkRDB', function(message){

        client.set(message.ID, socket.id);
        console.log("user is redis now with " + message.ID + " mysqlID and " + socket.id + " socketID :D");

    });
});
