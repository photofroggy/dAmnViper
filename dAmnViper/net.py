''' dAmnViper.net module
    Created by photofroggy.
    
    This module provides classes used to actually connect
    to dAmn using Twisted. The ConnectionFactory starts connections
    and handles disconnects. The IOProtocol handles basic IO operations
    on the connection, but delegates most of the processing to an
    instance of the dAmnSock class from the dAmnViper.base module.
'''

# Standard library
import time

# Twisted library imports
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory

# Viper stuff
from dAmnViper.parse import Packet


class ConnectionFactory(ClientFactory):
    """ This is the Connection class. It handles the basic functionality
        of the connection between the bot and dAmn's server.
    """
    
    stdout = None
    debug = None
    client = None

    def __init__(self, client, stdout=None, debug=None):
        """Initialise up in this motherfucka"""
        self.log = stdout
        self.debug = debug
        self.client = client
        
        if self.log is None:
            self.log = lambda m: None
        if self.debug is None:
            self.debug = lambda m: None
    
    def startedConnecting(self, connector):
        self.log('** Opening connection to dAmn...')
        self.client.connection.attempts = 1
    
    def create_protocol(self):
        return IOProtocol(self, self.client, self.stdout, self.debug)
        
    def buildProtocol(self, addr):
        protocol = self.create_protocol()
        self.client.set_protocol(protocol)
        return protocol
    
    def clientConnectionLost(self, connector, reason):
        self.log('** Connection closed.{0}'.format(
            ' Reason: {0}'.format(reason) if isinstance(reason, str) else ''))
        
        self.client.set_protocol(None)
    
    def clientConnectionFailed(self, connector, reason):
        self.log('** Failed to connect.{0}'.format(
            ' Reason: {0}'.format(reason) if isinstance(reason, str) else ''))
        
        if self.client.connection.attempts == self.client.connection.limit:
            self.log('** Failed to connect {0} times in a row.'.format(
                self.client.connection.attempts))
            self.client.set_protocol(None)
            return
            
        self.client.flag.retry = True
        self.client.set_protocol(None)


class IOProtocol(Protocol):
    
    conn = None
    client = None
    log = None
    debug = None
    __buffer = None
    
    def __init__(self, conn, client, stdout=None, debug=None):
        """ Initialise the protocol. """
        # Store our objects
        self.conn = conn
        self.client = client
        self.log = stdout
        self.debug = debug
        self.__buffer = ''
        
        # Make sure we have callables for logging stuff.
        if self.log is None:
            self.log = lambda m: None
        
        if self.debug is None:
            self.debug = lambda m: None
    
    def connectionMade(self):
        """ We have connected to the server! Send a handshake! """
        if not self.client.flag.connecting:
            return
        
        self.client.flag.shaking = True
        pkt = '{0}\nagent={1}\n{2}'.format(
            self.client.CONST.CLIENT, self.client.agent,
            '\n'.join(['{0}={1}'.format(
                    key, self.client.info[key]
            ) for key in self.client.info]))
        
        self.send_packet(pkt)
    
    def dataReceived(self, data):
        """ Handle incoming data. """
        
        # Split on null.
        self.__buffer+= data
        raw = self.__buffer.split('\0')
        self.__buffer = raw.pop()
        
        for chunk in raw:
            packet = Packet(chunk)
            
            # If it's a ping packet, send a pong straight away!
            if packet.cmd == 'ping':
                self.send_packet('pong\n')
            
            # Let the client do whatever it needs to with the packet.
            self.client.handle_pkt(packet, time.time())
    
    def send_packet(self, data):
        """ Send a packet to dAmn. """
        data = '{0}\0'.format(data)
        self.transport.write(data)
        return len(data)


# EOF
