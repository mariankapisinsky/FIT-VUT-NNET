/**
 * @file Async/wait echo server that converts received
 * messages to uppercase (TCP).
 * @author xkapis00
 */

const net = require('net');
const { argv } = require('process');

var port = 2022;
 
if ( argv.length === 3 ) port = argv[2];

function wait_for_connection ( server ) {

    return new Promise ( (resolve) => {
        server.once('connection', resolve);
    });
}

function wait_for_data ( socket ) {

    return new Promise ( (resolve) => {
        socket.once('data', resolve);
        socket.once('close', resolve);
    });
}

async function run ( server ) {

    console.log('Waiting for connection...');

    let socket = await wait_for_connection(server);

    let name = socket.remoteAddress + ":" + socket.remotePort;

    console.log('Connection from ' + name);

    run( server );

    await do_work( socket );

    console.log("Connection from " + name + " closed");
}

async function do_work( socket ) {

    let name = socket.remoteAddress + ":" + socket.remotePort;

    while ( true) {

        console.log('Waiting for data from ' + name);
        
        let data = await wait_for_data( socket );

        if ( !data ) break;
        
        console.log('Receveid: ' + data);

        data = data.toString().toUpperCase();
            
        await socket.write(data);
            
        console.log('Uppercased data sent back to: ' + name);
    }

}

const server = net.createServer()

server.listen( port, '127.0.0.1', { reuseAddr: true } );

run( server )