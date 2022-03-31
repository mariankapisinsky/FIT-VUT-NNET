/**
 * @file Simple echo client (TCP).
 * @author xkapis00
 */

const net = require('net');
const dns = require('dns');
const { argv, exit } = require('process');
const readline = require('readline');

var host = '127.0.0.1';
var port = 2022;

if ( argv.length === 4 ) {

    dns.lookup( argv[2], { family: 4 }, function ( err, address ) {
            
        if ( err ) {

            console.log( err );
            exit( 1 );

        }
        else {

            host = address;
            
        }

    });
    
    port = argv[3];
}

var client = new net.Socket();

client.connect( port, host, () => {

	console.log( 'Connected.' );

    var stdin = readline.createInterface( process.stdin );

    stdin.on( 'line', ( line ) => {

        client.write( line );

    });

    stdin.on( 'close', () => {

        client.destroy();

    });

});

client.on('data', ( data ) => {

	console.log( data.toString() );

});

client.on('close', () => {

	console.log( 'Connection closed.' );

});
