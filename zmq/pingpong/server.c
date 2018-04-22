#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <zmq.h>

int main(void) {
  void *context = zmq_ctx_new();
  void *rep = zmq_socket(context, ZMQ_REP);
  int rc = zmq_bind(rep, "tcp://*:9191");
  assert(rc == 0);

  while (1) {
    char buffer[5];
    zmq_recv(rep, buffer, 4, 0);
    buffer[4] = '\0';
    printf("Received request: %s\n", buffer);
    sleep(1);  //  Do some 'work'
    zmq_send(rep, "pong", 4, 0);
  }
  return 0;
}
