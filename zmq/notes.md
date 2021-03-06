The internet has no middle. That's why it works so well! 
And it does work almost miraculously well if you stop and think about it. 
I can put a little box under my desk and make it accessible to a friend in Australia.
Did you ever have to consider sharks in *your* application risk analysis?
There are some key resources you need and systems to pass through for that to happen, but there is no master organizer or coordinator to that connection.
There is no middle.

What if we could write applications that are as robust and flexible as the internet itself?
Could we do it without shaving the world's largest herd of Yaks?

Today we're going to talk about ZeroMQ, and how it can help us write robust and flexible networked and other concurrent applications.

First, a little about myself.
I work at Aurora Innovation, a self driving car startup here in Pittsburgh and Silicon Valley.
Previously I worked at Carnegie Mellon making robots slightly less broken.

Autonomous vehicles and other robots are unique kinds of distributed systems.
They generally have many connected components and systems working together onboard, but also often need to "call home" to fetch data, report locations, or coordinate actions.
They're quite literally little data centers on wheels.
Robots are distributed systems without middles.

So what is ZeroMQ?

ZeroMQ is an embedded networking library.
But that doesn't get at what it really does for us.
ZeroMQ's most important feature is that it makes extremely tedious and difficult networking tasks easy enough that you can start thinking about your architecture at a higher level.
Ways in which your components communicate and coordinate.
ZeroMQ calls these patterns.
What's more you can go from idea, to prototype, to production quickly.

We'll talk more about how ZeroMQ does its work in a minute, but let's look at some patterns we're familiar with.

The most common architecture most of us deal with is the standard web server thin client.

Often that's not enough, so we'll throw in a database, and maybe some load balanced servers.

This is already a complex architecture in many ways.
The load balancing has to be configured somewhere, which also drives how you manage state, and deploy architecture.
But this is really still a simple flow of thin clients doing display or data entry, some clever servers (or certainly complex, with a full HTTP stack), and a big fat cannot-fail database at the back.

Often, this is still not enough.
Servers usually can't do their jobs themselves.
They need to talk to other APIs, or offload some processing.

Or maybe we have a bunch of peers that need to communicate.
We could send them through a central server, but why centralize and add a single point of failure when it isn't necessary?
As long as we can identify each other, why can't we just talk directly?

Instead of the STAR topology that is very reliable only as long as the hub is up, and doesn't scale well directly, you get a (potentially) fully connected simplex that is robust to "hub" failure as long as you were able to identify one other peer.

What about the internet?

It was designed to be decentralized.
If a Russian bomb took out one node, the millitary and government could still communicate.

Now, you have a huge web of peers of different sizes, each serving some function.
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

You also don't get error handling, retry, or uniform behavior on different platforms.
I'm tired just thinking about it. And I haven't even started thinking about my architecture.


<!-- TODO: slide -->
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
And not just because it's Python either.
The C version is the same length.
And ZeroMQ has bindings for tons of languages.

It's also easy to integrate into any kind of project, being just a single library with no dependencies.
It's licensed under LGPL BUT with a static linking exception.
So no matter how you're packaging or delivering software, even closed source, as long as you don't modify ZeroMQ itself you are safe.

Let's go back to our first example now and talk about how ZeroMQ works.

The first API is the Context object.
The context is what you use to create sockets.
They are also the one ZeroMQ type you an share between threads.


Now ZeroMQ's core concept is called a socket.
These are not standard sockets, but the metaphore is ok.
There are different types of sockets that provide different communication patterns.

In our example we use the request (REQ) and reply (REP) socket types to get a two-way, RPC-like pattern.
This is just like a function call.
You provide some arguments, and get a result.
Usually a "server" or more stable, static, or known part of your architecture is acting as the reply socket (a receiver of requests).

All socket types must "bind" and "connect."
One side of the pair binds, and the other connects.
It generally doesn't matter which side does which, or which happens first.

Both our send and receive block here, though there is also a polling mechanism if you want to manage a collection of sockets or query message status.
Most real world applications won't use reply directly, but a router socket we'll describe below, or some more advanced pattern to handle server failure and application-level retry.


The next socket types are publish and subscribe.
This is simple one-way N to M broadcasting.
This is the simplest communication mechanism, and is basically used when you want to publish information without expecting a response.
You don't even know who's listening.

# Pro Tip: Don't implement RPC over Pub/Sub

A word of caution.
Know when you want RPC and when you want broadcasting.
If clients end up implementing spin-wait logic for a request that may never come you're in for some pain.


Next we have push and pull.

This is a one-way pattern like publish and subscribe, but with receiver round-robining.
That means that whenever a message is pushed, it is pulled by one next available puller.


Now there are other more complex socket types as well that we can only cover briefly here, but are important for more complex topologies.

The XPUB and XSUB sockets are just like their pub/sub counterparts but they also pass along subscription information.
When a socket connects or drops for example.
You can use this to create routers or proxies by forwarding messages along to another socket transparently.
This is such a common pattern ZeroMQ actually provides a helper function for creating a transparent proxy just like this.


<!-- TODO: proxy slide -->
The DEALER and ROUTER socket types are like reply and request sockets with N to M round robining.
That means you can serve requests to multiple different "servers" to do the work, and because of some extra routing metadata the answer gets back to the right requestor.

You can also get a native TCP streaming socket, in case you want to get really nasty and work directly w/ TCP packets.


Whew.
That was a lot.
There are actually several more socket types, some of which are preferred instead of the above types in recent versions of ZeroMQ, so I highly recommend you check out the ZeroMQ socket documentation.
However, these types form a core conceptual basis for how ZeroMQ works and what it can do.

Now. Let's step back and look at a couple of use cases for these sockets.


<!-- TODO: real example -->
We have our ping pong example for request and reply.
You can imagine a lot of REST APIs where you're not really posting a document but invoking some action on a server somewhere and getting a response (even if it's just a success or failure code).
RPC is an old but excellent mechanism.


Alright, now let's do a bunch of compute intensive processing.
Say we want to process a bunch of images.
The images could come from any source, but let's say there are a bunch of them or they're coming in fast.
This is a great case for a push/pull setup.
Your image source or job dispatcher pushes image data, and you have a bunch of compute resources online pulling and doing the processing.
Those pullers can publish their results to some aggregator for storage or further processing.

In the batch processing scenario, there's a gotcha to watch out for.
You may send the first puller to come online a bunch of messages before the rest get a chance to come up.
In this case, you'll want a notification mechanism that all consumers are ready.
Similiarly, you may want to know when you're done processing your batch so you can clean up and exit.
Maybe your compute resources are expensive.
This is a very common pattern in supercomputer programming.

If instead of batch processing you have a stream of incoming images to process, you could also implement your own elastic scaling.
Your source node can register how many items it has to process, or how large its backlog is, and request more processing nodes be stood up.


Ok, now, let's go deeper.

What happens when you actually send a message?
ZeroMQ takes your message and puts it in a message queue.

Then background I/O worker threads actually push your message out over your selected transport.
Background threads are NOT one per client or one per connection.
They are per socket based on volume of transmitted data.
As a rule of thumb you'll want one worker thread per GB of data sent per second.

The message queue means the actual I/O work happens asynchronously.
Nifty.

Messages are atomic blobs of data that are sent and received together or not at all.
They can be any size, gigabytes, as long as they fit in memory.

Messages can be broken into frames to deliminate different parts of the message.
However, they're still sent and received as one.
Frames make it easy to add routing or filtering envelopes.

Next we hit the transport layer.
Most networked solutions will use a TCP transport, but IPC, inprocess, and PGM are also options.
So, if you're doing all your work on a single computer, you don't have to pay the cost of sending messages to yourself over the network.
If you're doing all your work in a single *process*, then you can use the inprocess transport and ZeroMQ becomes a concurrency framework.

ZeroMQ scales wonderfully in this way.
Whatever your compute requirements are or environment is, you can scale the same code from threads, to processes, to different hosts.

<!-- TODO: zen-master enlightenment joke here? -->

Finally, on the other side of the connection (ZeroMQ has handled routing the message to the appropriate connection for us), worker threads enqueue the message again until you call receive.


Now you might be wondering what happens when things go wrong, because the first rule of networking is

# Things Will Fail

If a connection is lost ZeroMQ will intelligently attempt automatic reconnect.

If a message send fails, it will retry.

If it decides there is no hope it will return an error in the standard way for your programming language.

If ZeroMQ encounters an internal error it will immediately ASSERT and crash.

This is ZeroMQ's error handling philosophy.

# Be robust to external errors. Be intollerant of bugs.

Now what happens if while we're retrying old messages we're still sending new ones?
Or if the network is fine but our workers are overwhelmed and not able to respond fast enough?

All the ZeroMQ message queues have a configurable "high water mark."
That is, the queues have a max size.
Behavior when a particular socket's queue is full is well defined.
A pub or router socket will drop new sent messages, all other socket types will block.
Of course there are options to check that you will block and handle these cases yourself.


Now, I've mentioned the fact that ZeroMQ can be used between local processes or threads.
Using the inter-process communication transport saves a lot of network overhead, but you can still build better fault tolerance into your application with process isolation.
What that means, is if one process throws and exception, faults, halts, deadlocks, or otherwise crashes it won't take all your other processes down with them.
Such are the guarantees of an operating system.
The Erland "let it crash" philosophy works like this.

A great use case for IPC is plugin systems.
If you're writing an application you want to provide plugins for you generally have two options.
You can dynamically load a library compiled against a binary interface.
This is fast and fairly simple (it's just like calling any other code really), but what if you want users or other unknown third parties to supply plugins?
In that case, you might choose to use IPC and separate plugins as independent processes.
You provide a library and a way of building and registering the plugin, and then launch it at runtime and use message passing to interact with it over some protocol you define.

You could also just provide the server as the public API, allowing any external to interact with your program.
If anyone has been following the language server protocol work in Rust or at Apple with clangd that's a lot of the same motivations.

Another thing you can do is get actually truly safe in-process concurrency by switching to a message passing paradigm as well.
Instantiate a context in each thread and connect to an "inproc" transport and you're sending messages, potentially with zero copy, to other threads without shared mutable state.
ZeroMQ, once again, has taken care of the hard part of doing all the locking and atomic swapping of pointers.


Overall, ZeroMQ is about as good as network or parallel programming can get.


We've solved non-blocking I/O, dynamic connections, message buffering and congestion, transport transparent communication, message routing, and most classes of networking errors.

A library this simple yet powerful has deep implications for our application architectures.
Generally, two core patterns emerge.
Either message passing becomes central to an application (literally the core loop of a program) like an actor system, or fades quietly into the background like logging or metrics collection.

Ok, so we've talked a lot about what ZeroMQ can do for us, but there are still some unsolved problems.

The first is serialization.
What's our actual wire protocol?
ZeroMQ just sends raw bytes.
Fortunately you have lots of options here.
If you're in one language and ecosystem, you might already have a standard way of serializing messages.
If you're in the other extreme and need the absolute most maximum inoperability maybe you send json strings.

Many organizations have found serialization-first libraries to be very effective.
Google's protobuf library is a popular and robust choice.
You specify your data structure in a special definition language, and generate code for one or several client languages.
Then, you can serialize data with the protobuf libraries, send over the wire, and deserialize with consistency checks on the other end, even in a different programming language.
Here is an example of a generic image message, creating and send in both Python and C++.

One pro tip is you probably want to wrap your messages in some kind of envelope outside your actual serialized data.
Maybe a fixed size timestamp or counter.
Or a message type ID, size, or checksum.

Since ZeroMQ lets you break a single atomic message into multiple frames for easy chunking of data.
You can even have it automatically filter out messages by matching a byte prefix.

Discovery is another hard problem.
ZeroMQ requires you to provide an address and transport mechanism.

You could hard code it, but that will scale for about two days before falling apart.

You could deploy a configuration with your build.
This is simple and trackable, but then you can't update without a full redeploy.
This is a good time to reemphasize that ZeroMQ will attempt to reconnect if a connection goes away, so partial redeploys are very possible.

You could configure via command line or environmental variables and orchestrate at launch time.
This is a very docker-esque way of orchestrating systems, and there's good tooling for it.

You could use good old DNS if you control the network.
There are also centralized service discovery systems like etcd, Consul, or other simple key value stores where you only need to know one resource address to find all the others.
If you're actually doing some kind of consumer IoT you could also try your hand at implementing some UDP broadcast based discovery protocol.

All these approaches have their own advantages and tradeoffs, and you'll need to consider them as you build out your architecture.

Before we wrap up I'd like to discuss some alternatives to ZeroMQ, and when ZeroMQ might not be for you.

If you're just trying to do HTTP and document or REST style APIs, there are many great libraries and patterns to get the job done.
You can't implement or interop with HTTP with ZeroMQ because they have different wire protcols.

If you're only looking for an RPC solution, then gRPC (now owned by the Apache Foundation), is a battle tested and widely supported solution.
It carries some baggage and gotchas of its own however, and requires fairly modern infrastructure to do complex networking over TLS.

If you really actually want a true message queue or broker, especially one supporting MQTT (popular for IoT applications) consider RabbitMQ.

If you need a high performance streaming message framework, Apache Kafka might work well.

If you specifically need very lightweight pull-based metrics and monitoring, Prometheus has your back.

However.
If you need all of the above, some hybrid system or maybe something completely different, ZeroMQ can do it all.

I hope I've given you an idea of the kinds of things ZeroMQ enables.
You can rapidly prototype many kinds of distributed application topologies, and get them to production robustness without wizards.
You can define the protocol that works for your application.

More than anything else, this actually makes network programming fun, and I hope you go home or go to work and try to build something that talks to something else.

Finally, I'd be doing you a major disservice if I didn't direct you to dig into the official ZeroMQ documentation called "The Guide."
It's quite an incredible resource on network programming patterns in general, even if you don't use ZeroMQ itself.


Now, that's the end of my presentation.
I'm happy to take any questions now with the group, but please feel free to get up and walk around or leave.
I'll also be hanging around for a while to chat afterwords.

Thank you.

<!-- TODO: lazy pirate -->
<!-- TODO: msg Q? -->
<!-- TODO: zen joke? -->
