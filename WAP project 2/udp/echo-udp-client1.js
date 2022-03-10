/**
 * @file Simple connected echo client (UDP).
 * @author xkapis00
 */

 const dgram = require('dgram');
 const dns = require('dns');
 const { argv, exit } = require('process');
 const readline = require('readline');
 
 var host = '127.0.0.1';
 var port = 2022;
 
 if ( argv.length === 4 ) {
 
     dns.resolve4(argv[2], function( err, records ) {
         if ( err ) { 
             console.log(err);
             exit(1);
         }
         else {
             host = records[0];
         }
     });
 
     port = parseInt(argv[3], 10);
 };
 
 var client = dgram.createSocket('udp4');
 
 client.connect(port, host, function() {
 
     console.log('Connected');
 
     var stdin = readline.createInterface( process.stdin );
 
     stdin.on( 'line', function ( line ) {
 
         client.send(line);
     });
 
     stdin.on( 'close', function () {
 
         client.close();
     });
 
 });
 
 client.on('message', function( msg ) {
 
    console.log(msg.toString());
 });
 
 client.on('close', function() {
 
    console.log('Connection closed');
 
 });
 