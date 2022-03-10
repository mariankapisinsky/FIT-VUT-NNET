/**
 * @file Simple echo server that converts received
 * messages to uppercase (UDP).
 * @author xkapis00
 */

const dgram = require('dgram');
const { argv } = require('process');

var port = 2022;

if ( argv.length === 3 ) port = argv[2];

var server = dgram.createSocket( 'udp4' );

server.on( 'message', function ( msg, info ) {

    console.log('Received %d bytes from %s:%d\n', msg.length, info.address, info.port);
    
    msg = msg.toString().toUpperCase();

    server.send(msg, info.port, info.address);
  
});

server.on('listening', function() {

    console.log('Running...');
});

server.bind(port);