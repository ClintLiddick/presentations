#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import time

import zmq

from image_pb2 import Image as ImageMsg


def main(push_bind_loc, source_dir):
    ctx = zmq.Context.instance()
    push = ctx.socket(zmq.PUSH)
    push.bind(push_bind_loc)
    logging.info('bound')

    # wait for workers to spin up before starting
    time.sleep(1.0)

    # source of incoming images
    for imgname in os.listdir(source_dir):
        imgpath = os.path.join(source_dir, imgname)
        if not os.path.isfile(imgpath):
            continue
        logging.info('sending {}'.format(imgpath))
        with open(imgpath, 'rb') as imgfile:
            msg = ImageMsg()
            msg.original_filename = imgname
            msg.image_data = imgfile.read()
            # Send message. Will block until a worker accepts it.
            push.send(msg.SerializeToString())

    # finished
    push.close()
    ctx.term()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-s',
        '--source_dir',
        required=True,
        help='directory to send images from')
    parser.add_argument('push_socket', help='location to bind push socket to')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info('starting')

    sys.exit(main(args.push_socket, args.source_dir))
