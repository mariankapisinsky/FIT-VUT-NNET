/**
 * @file Multicast sender.
 * @author xkapis00
 */

const dgram = require('dgram');
const { argv, exit } = require('process');
const readline = require('readline');

if ( argv.length === 5 ) {
 
    var maddr = argv[2];
 
    var port = argv[3];

    var ttl = parseInt( argv[4], 10);
}
else {
    console.log("Usage: node multicast-sender.js <multicast IP address> <port> <ttl>");
    exit(1);
}

var sender = dgram.createSocket( { type: 'udp4', reuseAddr: true } );

sender.bind(port, function () {

    sender.setMulticastTTL(ttl);
    sender.setMulticastLoopback(true);
});

console.log('Socket created');
  
sender.on('message', function( msg ) {
 
    console.log(msg.toString());
});
 
sender.on('close', function() {
 
    console.log('Socket closed');
});
 
var stdin = readline.createInterface( process.stdin );
 
stdin.on( 'line', function ( line ) {
 
    sender.send(line, port, maddr);
});
 
stdin.on( 'close', function () {
 
    sender.close();
});