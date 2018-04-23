import zmq

def run_client(context, connect_addr):
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, '')  # no filter, i.e. subscribe to all
    socket.connect(connect_addr)

    while True:
        msg = socket.recv()
        print(msg)
        # do stuff...

def run_server(context, bind_addr):
    socket = context.socket(zmq.PUB)
    socket.bind(bind_addr)

    while True:
        # do stuff...
        msg = 'data'
        socket.send(msg)


def main_server():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr')
    args = parser.parse_args()
    
    ctx = zmq.context()
    run_server(ctx. args.addr)

def main_client():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr')
    args = parser.parse_args()
    
    ctx = zmq.context()
    run_client(ctx. args.addr)

def main_threaded():
    
