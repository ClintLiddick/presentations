#!/usr/bin/env python3

import time

import zmq

def main():
    ctx = zmq.Context.instance()
    rep = ctx.socket(zmq.REP)
    rep.bind('tcp://127.0.0.1:9191')

    msg_cnt = 0

    while True:
        msg = rep.recv()
        msg_cnt += 1
        print('Received request {}: {}'.format(msg_cnt, msg))
        time.sleep(0.5)
        rep.send(b'pong')
    

if __name__ == '__main__':
    main()
