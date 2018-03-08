# ZeroMQ
**Communication beyond HTTP**

Notes:
35 mins

---

## ZeroMQ
Sockets on steroids

#### Use Cases

- Large scale networked communication.
- RPC
- Multi-threading/multi-processing concurrency.
- Lightweight logging or metric aggregation.
- Architecture prototyping.
- Robust plugin systems.

Notes:
- HTTP and RESTful communication architectures are overemphasized to the exclusion of other networking patterns and technologies.
- ZeroMQ is a networking library with an emphasis on simplicity.

---

## HTTP
What it's good at

<!-- TODO: big complex server small clients diagram -->

Notes:
- Thin client / complex server oriented

---

## HTTP
What we often want

<!-- TODO: diagram: many medium complexity peers, with some thin leafs. -->
<!-- TODO: Plausible names for components -->

Notes:

---

## HTTP
What usually happens

<!-- TODO: diagram: layers of server + nginx and clients + varying embedded library/frameworks -->


Notes:

HTTP is not simple to implement, and while most languages and application frameworks have an HTTP client, embedding an HTTP server in an application is neither trivial nor consistent across languages.
And it usually requires running an additional server application (nginx, Apache) in front anyway.

- "Standalone" server requires libmicrohttpd, FastCGI, uWSGI
    - Usually need to stand up secondary HTTP server frontend like nginx or Apache anyway.

---

## Sockets

- Connect or wait for connection
- Send some data (TCP, UDP, etc.)
- Impose no protocol
- Extremely complex in the details
    - Error handling (reconnects)
    - Multiple connections
    - Interop/inconsistencies
    - All the other complexities of designing architecture and protocol

Notes:
- The problem is an imposed protocol and structure that we shoehorn our own protocols into/on top of
- Let's go down a level and see what's what
- https://beej.us/guide/bgnet/html/multi/clientserver.html
- That sockets are a better metaphore for many applications is evident in the rise of WebSockets, which recreates traditional socket programming in JavaScript.

---

## ZeroMQ

<!-- ZMQ logo -->

- "Sockets on steroids"
- Embedded networking library
- Concurrency framework

---

## Ping Pong Example

https://github.com/ClintLiddick/presentations/tree/master/zmq/pingpong

Notes:
- Short not just because of Python. C version only slightly longer because of error handling.

---

## Bindings

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

---

## What Problems Does ZMQ "Solve"?

- Non-blocking I/O <!-- .element: class="fragment" -->
- Dynamic connections <!-- .element: class="fragment" -->
- Message buffering and congestion <!-- .element: class="fragment" -->
- Swapping transports <!-- .element: class="fragment" -->
- Message routing <!-- .element: class="fragment" -->
- Network errors <!-- .element: class="fragment" -->

Notes:
- Why we need zmq: http://zguide.zeromq.org/page:all#toc18

---

## Implications

Simple reliable message passing becomes
1. central to an application <!-- .element: class="fragment" -->
1. quietly auxillary for logging or metrics <!-- .element: class="fragment" -->
    <!-- - HWM and drop -->

Notes:
- what does a library this simple yet powerful mean for our application architecture?

---

## Core Socket Types

- publish/subscribe <!-- .element: class="fragment" -->
    - one-way
- request/reply <!-- .element: class="fragment" -->
    - two-way
- push/pull <!-- .element: class="fragment" -->
    - one-way round-robin

Notes:
- http://api.zeromq.org/4-1:zmq-socket

---

## Auxillary Socket Types

- xpub/xsub
    - one-way with subscription information
- dealer
    - N-M round-robin reply side
- router
    - N-M round-robin request side
- pair
    - in-process exclusive pair

Notes:
- also native TCP stream

---

## How ZMQ Works

[The Guide](http://zguide.zeromq.org/page:all)

Notes:
- incredible resource for network programming patterns
- zmq example code
- http://zguide.zeromq.org/page:all#Missing-Message-Problem-Solver

---

## How ZMQ Works

Like sockets but not.
- Connections are 1-N <!-- .element: class="fragment" -->
- Many underlying transports including in-process, PGM <!-- .element: class="fragment" -->
- Automatic re-connect and retry when sensible <!-- .element: class="fragment" -->

Notes:
- Pragmatic General Multicast
    - multi-receiver file transfer

---

## How ZMQ Works

Queued and Async I/O
- Background thread for I/O <!-- .element: class="fragment" -->
- Message queues <!-- .element: class="fragment" -->
    - send, receive, or both sides
- Configurable "high water mark" <!-- .element: class="fragment" -->

Notes:
- 1 I/O thread per GB/s, not 1 thread per socket or per connection
- PUB/ROUTER will drop on HWM, others will block
- PUB/PUSH only send buffers
- SUB/PULL/REQ/REP only receive
- DEALER/ROUTER/PAIR send and receive

---

## How ZMQ Works

Error handling philosophy
- Internal error: assertion/exception
- External error: handle and/or return error code

Notes:
- http://zguide.zeromq.org/page:all#Handling-Errors-and-ETERM
        
---

## Sending Complex Data

- message
    - atomic blob of data that is sent/received together or not at all
- frame
    - a single part of a message. May be used to deliminate parts of a message.
    
**A message must always be able to fit in memory!** <!-- .element: class="fragment" -->
    
---
    
## Sending Complex Data

Frames can be used to easily implement
- routing evelopes
- filterable "IDs"

---

## Sending Complex Data

Google Protocol Buffers <!-- .element: class="fragment" -->
- language agnostic <!-- .element: class="fragment" -->
- robust serialization <!-- .element: class="fragment" -->

Notes:
- many choices

---

## Configuration vs. Discovery

- Orchestration <!-- .element: class="fragment" -->
    - Command line arguments
    - Environmental variables
    - Docker
- Centralized Discovery <!-- .element: class="fragment" -->
    - etcd
    - Consul
- Dynamic Discovery <!-- .element: class="fragment" -->
    - Custom? I don't know man.
    - IOT something something
    
Notes:
- zmq does not solve the service discovery problem

---

## Examples

- Parallel image processing
    - TCP and multi-threaded in-process
- Robust Plugin Architecture via IPC

---

## Parallel Image Processing
<!-- TODO -->
- thumbnail images
- signal to start

---

## Parallel Image Processing
Part Deux:  Multithreaded
<!-- TODO -->
- same as above

---

## IPC Plugin System
<!-- TODO -->
- req/rep when "server" dies? timeout?
- messaging-based api for plugins
- executor wraps plugin libs
- launch each registered plugin and run a socket for each

---

## FAQs

**What is the license?**

LGPLv3 with a static linking exception.

---
