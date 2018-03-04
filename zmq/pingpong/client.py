#!/usr/bin/env python3

import time

import zmq

def main():
    ctx = zmq.Context.instance()
    req = ctx.socket(zmq.REQ)
    req.connect('tcp://127.0.0.1:9191')

    while True:
        time.sleep(0.5)
        req.send(b'ping')
        msg = req.recv()
        print('Received response: {}'.format(msg))
    

if __name__ == '__main__':
    main()
