/**
 * @file Multicast listener.
 * @author xkapis00
 */

const dgram = require('dgram');
const { argv, exit } = require('process');

if ( argv.length === 4 ) {
 
    var maddr = argv[2];
    var port = argv[3];

}
else {

    console.log( 'Usage: node multicast-sender.js <multicast IP address> <port>' );
    exit( 1 );

}

var listener = dgram.createSocket( { type: 'udp4', reuseAddr: true } );

listener.on( 'message', ( msg, info ) => {
    
    console.log( 'Received %d bytes from %s:%d : %s', msg.length, info.address, info.port, msg.toString() );
    
});

listener.on( 'listening', () => { console.log( 'Listening...' ); });

listener.on( 'close', () => {

    listener.dropMembership( maddr );
    console.log( 'Socket closed.' );

} );

listener.bind( port, () => {

    listener.addMembership( maddr );

});
