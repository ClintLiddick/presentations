import glob
import os

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build_py import build_py
from distutils.command.clean import clean
from distutils.spawn import find_executable


class build_py_and_proto(build_py):
    def run(self):
        self.run_command('protoc')
        build_py.run(self)


class CleanCmd(Command):
    user_options = [('files=', None, 'extra files to clean')]

    def initialize_options(self):
        self._cleanfiles = []
        self.files = ''
        self.clean_extensions = ['_pb2.py']
        # clean.initialize_options(self)

    def finalize_options(self):
        if self.files:
            for f in self.files.split(','):
                self._cleanfiles.extend(glob.glob('**/{}'.format(f)))
        for ext in self.clean_extensions:
            self._cleanfiles.extend(glob.glob('**/*{}'.format(ext)))
        # clean.finalize_options(self)

    def run(self):
        print('running clean_proto')
        for f in self._cleanfiles:
            # TODO
            # os.remove(f)
            print(f)
        # clean.run(self)


class _clean(clean):
    print('_clean')
    sub_commands = [('clean_prot', None)] + clean.sub_commands


setup(
    name='zmq_presentation',
    version='0.1.0',
    packages=[
        'pingpong',
        'image_processing',
    ],
    cmdclass={
        'clean_proto': CleanCmd,
        'clean': _clean,
    },
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
)
