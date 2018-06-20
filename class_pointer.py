import logging
from enum import IntEnum

class Test:
    def __init__(self, name='default'):
        self.name = name

class LogLevel():
    INFO = 1
    def level_to_name(self):
        return "abc"

    def log(self, msg):
        print(msg)


log = LogLevel()
log.log(msg='My name is %(name)s'%{'name': 'manh'})