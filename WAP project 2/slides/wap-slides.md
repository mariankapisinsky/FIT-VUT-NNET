# WAP: Sieťová komunikácia </br> v Node.js

Marián Kapišinský 

---

## Moduly

--

### Základné moduly  

- vystavané nad `EventEmitter`, tzn. programovanie je založené na spracovaní *udalostí*, tj. definicií *callback* funkcií

- nie je možné vytvoriť iteratívny server

- transportná vrstva:
    - *dgram* - poskytuje implementáciu UDP socketov
    - *net* - poskytuje API na tvorbu TCP serverov a klientov

- vyššie vrstvy:
    - *tls, dns, http, http2, https*

--

### Užívateľské (npm) moduly

- Príklady:
    - <a href="https://www.npmjs.com/package/socket.io" target="_blank">socket.io</a> (TypeScript) - obojsmerná komunikácia založená na udalostiach v reálnom čase
    - <a href="https://www.npmjs.com/package/raw-socket" target="_blank">raw-socket</a> (C++ addon) - implementuje raw sockety
    - <a href="https://www.npmjs.com/package/pcap" target="_blank">pcap</a> (C++ addon) - implementuje väzby na libpcap
    - <a href="https://www.npmjs.com/package/icmp" target="_blank">icmp</a>, <a href="https://www.npmjs.com/package/arp" target="_blank">arp</a>, ...

--

### Udalosti

- Zoznam možných udalostí:
    - dgram.Socket - close, connect, error, listening, message
    - net.Socket - close, connect, data, drain, end, error, lookup, ready, timeout
    - net.Server - close, connection, error, listening

---

## TCP klient/server

--

### Server

```js [6,16|8-14|3-4,18]
const net = require('net');

var host = '127.0.0.1'
var port = 2022;

var server = net.createServer( function ( socket ) {
	
	socket.on( 'data', function ( data ) {

		data = data.toString();

		socket.write( data.toUpperCase() );

	});

});

server.listen( port, host );
```

--

### Klient

```js [7|4-5,9,25|11|13-17|19-23|27-31]
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

Pozn.: Alternatívne sa dá použiť `net.createConnection()`.

---

## UDP klient/server

--

### Server

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

--

### Klient

```js [7|9-13|15|4-5,17-21|23-27]
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

Pozn.: Dá sa použiť aj `client.connect()` (viď. TCP klient).

---

## Multicast

--

### Multicast - príjemca

```js [4|2,6,10|1,8|12-17|1,18-22]
var maddr = argv[2];
var port = argv[3];
	
var listener = dgram.createSocket( { type: 'udp4', reuseAddr: true } );

listener.bind( port, () => {
    
    listener.addMembership( maddr );
    
});

listener.on( 'message', ( msg, info ) => {
    
    console.log( msg.toString() );
    
});

listener.on( 'close', () => {

    listener.dropMembership( maddr );

});
```

--

### Multicast - odosielateľ

```js [5|2,7,11|3,9-10|14|1-2,16-20|22-26]
var maddr = argv[2];
var port = argv[3];
var ttl = parseInt( argv[4], 10 );

var sender = dgram.createSocket( { type: 'udp4', reuseAddr: true } );

sender.bind( port, () => {

    sender.setMulticastTTL( ttl );
    sender.setMulticastLoopback( true );

});

var stdin = readline.createInterface( process.stdin );

stdin.on( 'line', ( line ) => {
    
    sender.send( line, port, maddr );

});

stdin.on( 'close', () => {
    
    sender.close();

});
```

---

## Broadcast

--

### Broadcast - príjemca

```js [3|5-15|1,17]
var port = argv[2];

var listener = dgram.createSocket( { type: 'udp4', reuseAddr: true } );

listener.on( 'message', ( msg, info ) => {

    console.log( msg.toString() );

    if ( msg.toString() === "END." ) {

        listener.close()

    }

});

listener.bind( port );
```

--

### Broadcast - odosielateľ

```js [4|6|1-2,8-12|14-18|2,20-24]
var baddr = argv[2];
var port = argv[3];

var sender = dgram.createSocket( { type: 'udp4', reuseAddr: true } );

var stdin = readline.createInterface( process.stdin );

stdin.on( 'line', ( line ) => {
    
    sender.send( line, port, baddr );

});

stdin.on( 'close', () => {
    
    sender.close();

});

sender.bind( port, () => { 
    
    sender.setBroadcast( true ); 

});
```

---

## Asynchrónny server

--

### Promise

- Promise je objekt reprezentujúci eventuelné úšpesné alebo neúspešné dokončenie asynchrónnej operácie.
 
- tri stavy:
    - *pending* - počiatočný stav
    - *fulfilled* - úspešné dokončenie operácie
    - *rejected* - zlyhianie

--

### Príklad

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

Prevzaté z https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise.

--

### Využitie pre asynchrónny server

```js []
function wait_for_connection ( server ) {

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

--

### Server

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

---

## Ďakujem za pozornosť!