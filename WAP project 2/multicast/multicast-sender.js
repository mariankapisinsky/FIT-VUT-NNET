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

function send_line ( line ) {
    
    sender.send(line, port, maddr);
    console.log( 'Sending %d bytes to %s:%d : %s', line.length, maddr, port, line );
}

var sender = dgram.createSocket( { type: 'udp4', reuseAddr: true } );

sender.on( 'close', () => {
    
    console.log('Socket closed');
});

sender.bind( port, () => {

    sender.setMulticastTTL(ttl);
    sender.setMulticastLoopback(true);
});

var stdin = readline.createInterface( process.stdin );

stdin.on( 'line', ( line ) => {
    
    send_line( line )
});

stdin.on( 'close', () => {
    
    sender.close();
});

console.log('Socket created');