# WAP: Sieťová komunikácia v Node.js <!-- .element: style="text-align: center; font-size: 72px"> -->

Marián Kapišinský <!-- .element: style="text-align: center;"> -->



## Moduly <!-- .element: style="text-align: center; font-size: 72px"> --> 


### Základné moduly <!-- .element: style="text-align: center; font-size: 36px"> --> 

- vystavané nad `EventEmitter`, tzn. programovanie je založené na spracovaní *udalostiach*, tj. definicií *callback* funkcií

- nie je možné vytvoriť iteratívny server

- transportná vrstva:
    - *dgram* - poskytuje implementáciu UDP socketov
    - *net* - poskytuje API na tvorbu TCP serverov a klientov

- vyššie vrstvy:
    - *tls, dns, http, http2, https*


### Užívateľské (npm) moduly <!-- .element: style="text-align: center; font-size: 36px"> --> 

Príklady:
- socket.io (TS)- obojsmerná komunikácia založená na udalostiach v reálnom čase
- raw-socket (C++) - implementuje raw sockety
- pcap (C++) - implementuje väzby na libpcap
- icmp, arp, ...



## TCP klient/server <!-- .element: style="text-align: center; font-size: 72px"> --> 


### Server <!-- .element: style="text-align: center; font-size: 36px"> -->

```js [3,13|5-11|14-18]
const net = require('net');

var server = net.createServer ( function ( socket ) {
	
	socket.on( 'data', function ( data ) {

		data = data.toString();

		socket.write( data.toUpperCase() );

	});

});

var host = '127.0.0.1'
var port = 2022;

server.listen( port, host );
```


### Klient <!-- .element: style="text-align: center; font-size: 36px"> -->

```js [7|4-5,9-25|27-31]
const net = require('net');
const readline = require('readline');

var host = '127.0.0.1'
var port = 2022;

var client = new net.Socket();

client.connect( port, host, function () {

    var stdin = readline.createInterface( process.stdin );

    stdin.on( 'line', function ( line ) {

        client.write( line );

    });

    stdin.on( 'close', function () {

        client.destroy();

    });

});

client.on('data', function ( data ) {

	console.log( data.toString() );

});
```



## UDP klient/server <!-- .element: style="text-align: center; font-size: 72px"> --> 


### Server <!-- .element: style="text-align: center; font-size: 36px"> -->

```js [3|5-11|13-15]
const dgram = require('dgram');

var server = dgram.createSocket( 'udp4' );

server.on( 'message', function ( msg, info ) {

    msg = msg.toString();

    server.send( msg.toUpperCase(), info.port, info.address );

});

var port = 2022;

server.bind( port );
```


### Klient <!-- .element: style="text-align: center; font-size: 36px"> -->

```js [7|9-12|14|4-5,16-19|21-24]
const dgram = require('dgram');
const readline = require('readline');
 
var host = '127.0.0.1';
var port = 2022;
 
var client = dgram.createSocket( 'udp4' );
  
client.on( 'message', function( msg ) {
 
    console.log( msg.toString() );
});
 
var stdin = readline.createInterface( process.stdin );
 
stdin.on( 'line', function ( line ) {
 
    client.send(line, port, host);
});
 
stdin.on( 'close', function () {
 
    client.close();
});
```

Pozn.: Dá sa aj použiť `client.connect( port, host, callback )` (viď. TCP klient). <!-- .slide: style="text-align: center;"> -->



## Multicast/broadcast <!-- .element: style="text-align: center; font-size: 72px"> -->


### Multicast <!-- .element: style="text-align: center; font-size: 36px"> -->


### Broadcast <!-- .element: style="text-align: center; font-size: 36px"> -->



## Asynchrónny server <!-- .element: style="text-align: center; font-size: 72px"> --> 


### Promise <!-- .element: style="text-align: center; font-size: 36px"> --> 

Promise je objekt reprezentujúci eventuelné úšpesné alebo neúspešné dokončenie asynchrónnej operácie.

 
Tri stavy:

- *pending* - počiatočný stav
- *fulfilled* - úspešné dokončenie operácie
- *rejected* - zlyhianie


### Príklad <!-- .element: style="text-align: center; font-size: 36px"> -->

```js [1-5|7-15|17,18|17,19|17,20|17,21|17,22]
function handleResolved ( value ) { 

    return value + ' and bar';

}

const myPromise = new Promise ( ( resolve, reject ) => {

  setTimeout( () => {

    resolve( 'foo' );

  }, 1000);

});

myPromise
 .then( handleResolved ) // foo and bar
 .then( handleResolved ) // foo and bar and bar
 .then( handleResolved ) // foo and bar and bar and bar
 .then( value => { console.log(value) } )
 .catch( err => { console.log(err) } ); 
```


### Využitie pre asynchrónny server <!-- .element: style="text-align: center; font-size: 36px"> -->

```js []
function wait_for_connection( server ) {

    return new Promise ( ( resolve ) => {

        server.once( 'connection', resolve );

    });

}
```

```js [1,3-7,21|1,9-13,21|1,15-19,21]
function wait_for_data ( socket ) {

    const data = new Promise ( ( resolve ) => {

        socket.once( 'data', resolve );

    });

    const close = new Promise ( ( resolve ) => {

        socket.once( 'close', resolve );

    });

    return Promise.race( [data, close] ).then( ( value ) => {

        return value;

    });

}
```


### Server <!-- .element: style="text-align: center; font-size: 36px"> -->

```js [3,5,11|3,7,11|3,9,11|13,15,17,25,27|13,15,19,25,27|13,15,21,25,27|13,15,23,25,27|32|29-30,34|36]
const net = require('net');

async function run( server ) {

    let socket = await wait_for_connection( server );

    run( server );

    await do_work( socket );

}

async function do_work( socket ) {

    while ( true ) {
        
        let data = await wait_for_data( socket );

        if ( !data ) break;
    
        data = data.toString();
            
        await socket.write( data.toUpperCase() );
        
    }

}

var host = '127.0.0.1';
var port = 2022;

const server = net.createServer();

server.listen( port, host, { reuseAddr: true } );

run( server );
```