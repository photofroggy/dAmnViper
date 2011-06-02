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
    """ Connection management.
        
        Instances of this class are used by :py:class:`dAmnSock
        <dAmnViper.base.dAmnSock>` to connect to dAmn.
        
        The object returns instances of :py:class:`IOProtocol
        <dAmnViper.net.IOProtocol>` when a connection is made and
        handles disconnects and connection failures.
        
        This object should not be used directly by applications using
        dAmnViper.
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
        """ Called by twisted when we start to connect.
            
            All this method really does is display a message and set
            the connecting flag to ``True``.
        """
        self.log('** Opening connection to dAmn...')
        self.client.flag.connecting = True
    
    def create_protocol(self):
        return IOProtocol(self, self.client, self.stdout, self.debug)
        
    def buildProtocol(self, addr):
        """ Called by twisted when a protocol is needed.
            
            Twisted calls this method when a connection can be
            established with the server. This method creates an instance
            of the :py:class:`IOProtocol <dAmnViper.net.IOProtocol>`
            class. This instance is given to the :py:class:`dAmnSock
            <dAmnViper.base.dAmnSock>` object that the factory belongs
            to, and returned to twisted.
        """
        protocol = self.create_protocol()
        self.client.set_protocol(protocol)
        return protocol
    
    def clientConnectionLost(self, connector, reason):
        """ Called by twisted when a connection is lost.
            
            Displays a message notifying the connection loss and tells
            the :py:class:`dAmnSock <dAmnViper.base.dAmnSock>` object
            that there is no longer a connection open.
        """
        self.log('** Connection closed.{0}'.format(
            ' Reason: {0}'.format(reason) if isinstance(reason, str) else ''))
        
        self.client.set_protocol(None)
    
    def clientConnectionFailed(self, connector, reason):
        """ Called by twisted when we fail to connect properly.
            
            The behaviour of this method is similar to the
            ``clientConnectionLost`` method.
        """
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
    """ Protocol layer for the dAmn connection.
        
        Instances of this class are used to directly communicate with
        the connection to dAmn via twisted, and gives any data received
        to the :py:class:`dAmnSock <dAmnViper.base.dAmnSock>` instance
        being used for this connection.
        
        This object should not be used directly by applications using
        dAmnViper.
    """
    
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
        """ Called by twisted when we have connected.
            
            This method simply sends a handshake to the dAmn server, and
            sets the client's ``shaking`` flag to ``True``, indicating
            that a handshake packet has been sent.
        """
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
        """ Called by twisted when data is received.
            
            The data received is added to out buffer. If there are any
            full packets in the buffer, these packets are sent to the
            :py:class:`dAmnSock <dAmnViper.base.dAmnSock>` instance to
            be parsed properly.
            
            Any event handling relating to specific packet is done in
            ``dAmnSock`` instance.
        """
        
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
        """ A wrapper function for sending packets to the server.
            
            Here, a null character (``\\0``) is appended to the given
            data, and we return the number of characters we have tried
            send to the server.
        """
        data = '{0}\0'.format(data)
        self.transport.write(data)
        return len(data)


# EOF
