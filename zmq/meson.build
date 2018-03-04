project('zmq_presentation')

protoc = find_program('protoc')
protoc_py_command = [protoc, '-I', '@CURRENT_SOURCE_DIR@', '--python_out', './',
                     '@INPUT@']

test_proto_py = custom_target('test_proto_py',
                              output: '@BASENAME@_pb2.py',
                              input: 'test.proto',
                              install: true,
                              install_dir: '',
                              command: protoc_py_command)


install_subdir('pingpong', install_dir: '')
