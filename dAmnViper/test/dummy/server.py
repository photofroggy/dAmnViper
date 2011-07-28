''' dAmnViper.test.dummy.server module
    Created by photofroggy
    
    This module is intended to be used in conjunction with unit tests testing
    the Client objects provided in dAmnViper. Running this module as a script
    spawns a server which listens for connections over a TCP connection and sends
    a dAmn handshake packet when required. This is sufficient for testing the
    connective functionality of Client objects.
    
    Note that the server here is based on the echoserv example provided by
    Twisted Matrix Laboratories.
'''

import os
import sys
import os.path

os.chdir(os.path.dirname(__file__))
os.chdir('../../../')
sys.path.insert(0, os.getcwd())

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol

# Get the packet parser or some shit! Should help a little.
from dAmnViper.parse import Packet


class Dummy(Protocol):
    """ Dummy dAmn protocol implementation.
        
        This protocol object acts as a very simple implementation of a small
        part of the protocol. All this server needs to do is respond to
        handshakes sent by connected clients. May send an error back whenever
        something other than a handshake is received.
    """
    
    def __init__(self):
        self.__buffer = ''
    
    def dataReceived(self, data):
        """ Process data sent by clients. Stolen from ChatProtocol! """
        # Buffer data!
        self.__buffer+= data
        # Split on null.
        raw = self.__buffer.split('\0')
        self.__buffer = raw.pop()
        
        # We only want the handshake, everything else can be ignored for now.
        for chunk in raw:
            packet = Packet(chunk)
            
            if packet.cmd == 'dAmnClient':
                self.transport.write('dAmnServer 0.3\n\0')


def main():
    f = Factory()
    f.protocol = Dummy
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    main()
