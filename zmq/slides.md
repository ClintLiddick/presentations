# ZeroMQ: <small>Communication beyond REST</small>

Clint Liddick
January 01, 2018

---

## Test

blah


---

## Thesis

HTTP and RESTful communication architectures are overemphasized to the exclusion of other networking patterns and technologies.
ZeroMQ is a networking library with an emphasis on simplicity.
It has many use cases including:

- Large scale networked communication.
- RPC
- Multi-threading/multi-processing concurrency.
- Lightweight logging or metric aggregation.
- Architecture prototyping.
- Robust plugin systems.

## HTTP

HTTP is simple to use, but forces a single client/server architecture on applications and pushes other problems onto complex infrastructure (e.g. load-balancing).

Pros:
- Conceptually simple (at first)

Cons:
- Client/server oriented
    - dumb client complex server
- Standalone, libmicrohttpd, or FastCGI
- WebSockets add flexibility for browser apps, but not well supported

## Sockets

- Connect or wait for connection
- Send some data (TCP, UDP, etc.)
- Impose no protocol
- Extremely complex in the details
    - Error handling (reconnects)
    - Multiple connections
    - Interop/inconsistencies
    - All the other complexities of desining architecture and protocol

Notes:
https://beej.us/guide/bgnet/html/multi/clientserver.html

## ZeroMQ

- "Sockets on steroids"
- Single library, over 30 languages
- ping pong example [TODO]


<table style="font-size: .4em">
  <tr>
    <td>
8th<br>
Ada<br>
Bash<br>
Basic<br>
C<br>
Chicken Scheme<br>
Common Lisp<br>
C# (.NET & Mono)<br>
C++<br>
D<br>
delphi<br>
Eiffel<br>
Erlang<br>
F#<br>
Felix<br>
Flex (ActionScript)<br>
</td>
<td>
Fortran77<br>
Free Pascal Compiler<br>
Go<br>
Guile<br>
Haskell<br>
Haxe<br>
Java<br>
Julia<br>
LabVIEW<br>
Luas<br>
Metatrader 4<br>
Nimrod<br>
Node.js<br>
Objective-C<br>
Objective Caml<br>
ooc<br>
</td>
<td>
Perls<br>
PHP<br>
Python<br>
Q<br>
Racket<br>
R<br>
REBOL 2<br>
REBOL 3<br>
Red<br>
R (pbdR)<br>
Ruby<br>
Scala<br>
Smalltalk<br>
Swift<br>
Tcl<br>
    </td>
  </tr>
</table>

## Architecture

- Message passing becomes central to app
- Can also be auxillary for logging or metrics
    - HWM and drop
- Why we need zmq: http://zguide.zeromq.org/page:all#toc18

## Core Patterns

- http://api.zeromq.org/4-1:zmq-socket
- pub/sub
    - xpub/xsub
        - subscription passthrough
- req/rep
    - dealer/router
- push/pull
- pair

## Simple Example

- ping/pong

## How ZMQ Works

- Education: docs
- Technical
    - sockets under the covers, but not 1-to-1
        - binding/(re)connecting
        - TCP, UDP, IPC
        - inproc
    - background thread
		- http://zguide.zeromq.org/page:all#I-O-Threads
    - queuing on both sides
	- error handling
	    - http://zguide.zeromq.org/page:all#Handling-Errors-and-ETERM

## Sending Complex Data

- message and frame
    - filtering
    - multipart as envelope pattern
- protobuf
- this means you can invent any domain specific "protocol" you want
    - not just GET/PUT/POST/DELETE
        - is GET idempotent?
    - RPC

## Use Cases: parallel processing
- thumbnail images
- signal to start

## Use Cases: multi-threading
- same as above

## Use Cases: IPC plugins
- req/rep when "server" dies? timeout?
- messaging-based api for plugins
- executor wraps plugin libs
- launch each registered plugin and run a socket for each

## Configuration
- command line or "orchestration"
- local config (in-repo)
- centralized
- discovery
    - DNS
    - etcd


## FAQs

**What is the license?**

LGPLv3 with a static linking exception.
