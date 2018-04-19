The internet has no middle. That's why it works so well! 
And it does work almost miraculously well if you stop and think about it. 
I can put a little box under my desk and make it accessible to a friend in Australia.
Did you ever have to consider sharks in *your* application risk analysis?
There are some key resources you need and systems to pass through for that to happen, but there is no master organizer or coordinator to that connection.
There is no middle.

What if we could write applications that are as robust and flexible as the internet itself?
Could we do it without shaving the world's largest herd of Yaks?

Today we're going to talk about ZeroMQ, and how it can help us write robust and flexible networked and other concurrent applications.


So what is ZeroMQ?

ZeroMQ is an embedded networking library.
But that doesn't get at what it really does for us.
ZeroMQ's most important feature is that it makes extremely tedious and difficult networking tasks easy enough that you can start thinking about your architecture at a higher level.
Ways in which your components communicate and coordinate.
ZeroMQ calls these patterns.

We'll talk more about how ZeroMQ does its work in a minute, but let's look at some patterns we're familiar with.

The most common architecture most of us deal with is the standard web server thin client.

<!-- TODO: single server client RPC -->

Often that's not enough, so we'll throw in a database

<!-- TODO: single db + server + client RPC -->

and maybe some round-robined servers

<!-- TODO: single db + N servers + many (...) clients all RPC -->

This is already a complex architecture in many ways.
The round robining has to be configured somewhere, which also drives how you manage user state.
But this is really a simple flow of thin clients doing display or simple data entry, some clever (or certainly complex, with a full HTTP server) servers, and a big fat cannot-fail database at the back.

What about the internet?

<!-- massive web of db, huge med and small servers some of each of which are leaves, not all RPC -->

You have a huge web of peers of different sizes, each serving some function.
Huge routing and resolving tables, massive data sets being served, supercomputers churning away, sharded computation (like SETI@Home), medium and small services doing their thing, small peers sharing data, and billions of thin consumers.

It's quite a diverse thing.

How can we even get started?

Let's start where the wizards of old finished their work.
We have hardware, routing and switching, name resolution, and transport protocols like TCP.
So we're solidly in the application layer.
But still where do we start?

Ok, well let's start at the bottom.
At the bottom of the stack that we care about live sockets.
Sockets are (for the most part) one-to-one connections (with other sockets) over some transport layer.
How do we package data? Up to you.
What protocol do we use? You have to invent one.
What if we want to talk to multiple peers? You have to manage a pool of sockets.

For those who haven't had the pleasure, this is what opening a socket looks like.

<!-- beeji socket code -->

You also don't get error handling, retry, or uniform behavior on different platforms.
I'm tired just thinking about it. And I haven't even started thinking about my architecture.

What about HTTP? 
We use it all the time, maybe there's something there.
HTTP itself is not easy to implement, and while most languages and application frameworks have an HTTP client, embedding an HTTP server, a listener, in an application is neither trivial nor consistent.
Your main choices are something like libmicrohttpd, FastCGI, or uWSGI.
And it usually always requires running an additional server application like nginx or Apache in front of your real application anyway.
And now you're shoehorning your own protocol on top of document requests.
Paths, GET, POST, PUT, DELETE.
Even front-end JavaScript developers found this metaphore to be insufficient and implemented websockets!

So ZeroMQ.
It bills itself as "sockets on steroids."
The code is simple (I'll explain more what's going on in a moment).
We get:
- non-blocking I/O (it manages the background thread)
- Dynamic connections and automatic retry
- Message buffering and congestion handling
- A consistent API over mulitple transports, even local IPC and in-process
- Message routing
- Network errors

This code isn't simple just because it's Python either.
The C version is only a few lines longer because of error code checking.
And ZeroMQ has bindings for almost any language you could name

<!-- TODO: lang list -->

Let's go back to our first example now and talk about how ZeroMQ works.

ZeroMQ's core concept is called a socket.
These are not standard sockets, but the metaphore is ok.
There are different types of sockets that provide different communication patterns.

In our example we use the request (REQ) and reply (REP) socket types to get a two-way, RPC-like pattern.
Usually a "server" or more stable, static, or known part of your architecture is acting as the reply socket (the receiver of requests).
This is just like a function call.

<!-- TODO function signature fn: req -> rep -->

Both our send and receive block here, though there is also a polling mechanism if you want to manage a collection of sockets or query message status.

The next socket types are publish and subscribe.
<!-- TODO: slide? code example? -->
This is simple one-way N to M broadcasting.
This is the simplest communication mechanism, and is basically used when you want to publish information without expecting a response.
You don't even know who's listening.

# Pro Tip: Don't implement RPC over Pub/Sub

It's a good idea to have your publishing side use bind, and any subscribers use connect.
<!-- TODO: mention context and bind/connect first? -->

Next we have push and pull.
<!-- TODO: animation of msg getting sent (arrow) to different subscribers -->
This is a one-way pattern like publish and subscribe, but with receiver round-robining.
That means that whenever a message is pushed, it is pulled by one next available puller.

Now there are other more complex socket types as well that we can only cover briefly here, but are important for more complex topologies.

The XPUB and XSUB sockets are just like their pub/sub counterparts but they also pass along subscription information.
When a socket connects or drops for example.
You can use this to create routers or proxies by forwarding messages along to another socket transparently.

<!-- TODO: proxy diagram -->

The DEALER and ROUTER socket types are like reply and request sockets with N to M round robining.
That means you can serve requests to multiple different "servers" to do the work, and because of some extra routing metadata the answer gets back to the right requestor.

There is a PAIR type that is an exclusive one to one but two-way socket specifically for use by two different threads in the same process.
We'll talk about in and inter process usage in a moment.

You can also get a native TCP streaming socket, in case you want to get really nasty and work directly w/ TCP packets.


Whew.
That was a lot.

Let's step back and look at a couple simple examples using these sockets.

We have our ping pong example for request and reply.
You could imagine a lot of REST APIs where you're not really posting a document but invoking some action on a server somewhere and getting a response (even if it's just a success or failure code).
RPC is an old but excellent mechanism.

As a publish/subscribe example, let's a lightweight remote logging mechanism.

<!-- TODO: many servers with many pubishers with one aggregator -->


TODO: push/pull image processing (supercomputer)
TODO: img processing w/ notification later

...

Now you might be wondering what happens when things go wrong, because the first rule of networking is

# Things Will Fail


- introduce zmq core concepts
  - context
  - socket types
  - transport
  - error handling
- problems it solves
- implications
- how can we use this? example patterns (simple to complex)
- what is hard/unsolved?
  - serialization (we've been using just strings)
  - discovery


- new architectures and possibilities by breaking free of old patterns/tools (http)


# The first rule of networking: things will fail
