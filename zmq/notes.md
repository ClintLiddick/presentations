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


- introduce zmq core concepts
- problems it solves
- implications
- how can we use this? example patterns (simple to complex)
- what is hard/unsolved?
  - serialization
  - discovery


- new architectures and possibilities by breaking free of old patterns/tools (http)


# The first rule of networking: things will fail
