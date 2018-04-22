#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <zmq.h>

int main(void) {
  void *context = zmq_ctx_new();
  void *req = zmq_socket(context, ZMQ_REQ);
  zmq_connect(req, "tcp://127.0.0.1:9191");

  while (1) {
    char buffer[5];
    zmq_send(req, "ping", 5, 0);
    zmq_recv(req, buffer, 4, 0);
    buffer[4] = '\0';
    printf("Received response: %s\n", buffer);
  }
  zmq_close(req);
  zmq_ctx_destroy(context);
  return 0;
}
