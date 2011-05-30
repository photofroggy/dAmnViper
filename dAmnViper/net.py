''' dAmnViper.stream module
    This module is part of the dAmnViper package.
    Created by photofroggy.
'''

# Standard library
import time

# Twisted library imports
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory

# Viper stuff
from dAmnViper.parse import Packet


class ConnectionFactory(ReconnectingClientFactory):
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
        self.client.flag.connecting = True
    
    def create_protocol(self):
        return IOProtocol(self, self.client, self.stdout, self.debug)
        
    def buildProtocol(self, addr):
        protocol = self.create_protocol()
        self.client.set_protocol(protocol)
        return protocol
    
    def halt(self):
        # Because I'm a retard.
        self.stopTrying()
        if reactor.running:
            reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        self.log('** Connection closed.{0}'.format(
            ' Reason: {0}'.format(reason) if isinstance(reason, str) else ''))
        
        self.client.set_protocol(None)
        
        if not self.client.flag.reconnect:
            self.halt()
            return
        
        if self.client.flag.quitting or not self.client.flag.reconnect:
            self.halt()
            return
        
        if not self.client.authenticate():
            self.halt()
            return
        
        self.log('** Attempting to reconnect...')
        self.retry(connector)
    
    def clientConnectionFailed(self, connector, reason):
        self.log('** Failed to connect.{0}'.format(
            ' Reason: {0}'.format(reason) if isinstance(reason, str) else ''))
        
        self.client.set_protocol(None)
        
        if self.client.connection.attempts == self.client.connection.limit:
            self.log('** Failed to connect {0} times in a row.'.format(
                self.client.connection.attempts))
            self.halt()
            return
        
        if not self.client.authenticate():
            self.halt()
            return
        
        self.log('** Attempting to connect again...')
        self.client.connection.attempts+= 1
        self.retry(connector)


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
    
    def handle(self, data):
        """ Create the deferred for handling incoming data. """
        processor = defer.Deferred()
        processor.addCallback(self.client.handle_pkt_deferred)
        processor.callback(data)
    
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
            self.handle((packet, time.time()))
    
    def send_packet(self, data):
        """ Send a packet to dAmn. """
        data = '{0}\0'.format(data)
        self.transport.write(data)
        return len(data)


# EOF
