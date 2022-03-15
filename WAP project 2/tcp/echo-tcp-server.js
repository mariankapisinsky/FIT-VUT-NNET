/**
 * @file Simple echo server that converts received
 * messages to uppercase (TCP).
 * @author xkapis00
 */

const net = require('net');
const { argv } = require('process');

var server = net.createServer ( function ( socket ) {

	var name = socket.remoteAddress + ":" + socket.remotePort;

	console.log( 'Connection from %s.', name );
	
	socket.on( 'data', function ( data ) {

		data = data.toString();

		console.log( 'Received %d bytes from %s : %s', data.length, name, data );

		data = data.toUpperCase();

		socket.write(data);

		console.log( 'Sending %d bytes to %s : %s', data.length, name, data );
	});

	socket.on( 'close', function ( ) {

		console.log("Connection from " + name + " closed.");
	});

});

var port = 2022;

if ( argv.length === 3 ) port = argv[2];

server.listen( port, '127.0.0.1' );
console.log( 'Running on port %s...', port);