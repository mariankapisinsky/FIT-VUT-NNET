/**
 * @file Broadcast data from stdin to a local network.
 * @author xkapis00
 */

const dgram = require('dgram');
const { argv, exit } = require('process');
const readline = require('readline');
 
if ( argv.length === 4 ) {
  
    var baddr = argv[2];
    var port = argv[3];

}
else {

    console.log( 'Usage: node send-broadcast.js <broadcast IP address> <port>' );
    exit( 1 );
}

var sender = dgram.createSocket( { type: 'udp4', reuseAddr: true } );

sender.on( 'close', () => {
    
    console.log( 'Socket closed.' );

});

function send_line ( line ) {
    
    sender.send( line, port, baddr );
    
    console.log( 'Sending %d bytes to %s:%d : %s', line.length, baddr, port, line );

}

var stdin = readline.createInterface( process.stdin );

stdin.on( 'line', ( line ) => {
    
    send_line ( line );

});

stdin.on( 'close', () => {
    
    sender.close();

});

sender.bind( port, () => { 
    
    sender.setBroadcast( true ); 

});

console.log( 'Socket created.' );
