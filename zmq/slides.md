# ZeroMQ: <small>Communication beyond REST</small>

Clint Liddick
January 01, 2018

## Thesis

HTTP and RESTful communication architectures are overemphasized to the exclusion of other networking patterns and technologies. ZeroMQ is a networking library with an emphasis on simplicity. It has many use cases including:

- Large scale networked communication.
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
- Standalone, libmicrohttpd, or FastCGI
- WebSockets add flexibility for browser apps, but not well supported


## FAQs

**What is the license?**

LGPLv3 with a static linking exception.
