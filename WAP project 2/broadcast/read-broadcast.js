/**
 * @file Reads data sent to a broadcast address and given port until "END." is received.
 * @author xkapis00
 */

const dgram = require('dgram');
const { argv, exit } = require('process');

if ( argv.length === 3 ) {
 
    var port = argv[2];
}
else {

    console.log("Usage: node read-brodcast.js <port>");
    exit(1);
}

var listener = dgram.createSocket( { type: 'udp4', reuseAddr: true } );

listener.on( 'message', function ( msg, info ) {
    
    console.log( 'Received %d bytes from %s:%d : %s', msg.length, info.address, info.port, msg.toString() );

    if ( msg.toString() === "END." ) {
        console.log( 'Closing socket.' )
        listener.close()
    }
});

listener.on( 'listening', function () {
    
    console.log( 'Listening...' );
});

listener.bind( port );