/**
 * @file Simple echo client (UDP).
 * @author xkapis00
 */

const dgram = require('dgram');
const dns = require('dns');
const { argv, exit } = require('process');
const readline = require('readline');
 
var host = '127.0.0.1';
var port = 2022;
 
if ( argv.length === 4 ) {
 
    dns.lookup( argv[2], { family: 4 }, ( err, address ) => {
            
        if ( err ) {

            console.log( err );

            exit( 1 );
        }
        else {

            host = address;
        }
    });
 
    port = parseInt( argv[3], 10 );
};
 
var client = dgram.createSocket( 'udp4' );

console.log( 'Socket created.' );
  
client.on( 'message', ( msg ) => {
 
    console.log(msg.toString());
});
 
client.on( 'close', () => {
 
    console.log('Socket closed.');
});
 
var stdin = readline.createInterface( process.stdin );
 
stdin.on( 'line', ( line ) => {
 
    client.send( line, port, host );

});
 
stdin.on( 'close', () => {
 
    client.close();
});