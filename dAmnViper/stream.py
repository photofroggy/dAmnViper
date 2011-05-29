''' dAmnViper.stream module
    This module is part of the dAmnViper package.
    Created by photofroggy.
'''

import os
import time
import errno
import socket
from threading import Thread, BoundedSemaphore

class Connection(Thread):
    """ This is the Connection class. It handles the basic functionality
        of the connection between the bot and dAmn's server.
    """
    
    class server:
        """Server connection details."""
        host = None
        version = None
        port = None
    
    _charset = 'latin-1'
    _lock = None
    _runn = False
    _inn = False
    _debug = False

    def __init__(self, host='chat.deviantart.com', version='dAmnClient 0.3', port=3900, debug=False):
        """Initialise up in this motherfucka"""
        Thread.__init__(self)
        self.server.host = host
        self.server.version = version
        self.server.port = port
        self.sock = None
        self.packet = []
        self.__buffer = str()
        self._lock = BoundedSemaphore()
        self._debug = debug
    
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((socket.gethostbyname(self.server.host), self.server.port))
            self.sock.setblocking(0)
            self.sock.settimeout(.5)
        except socket.error:
            self.sock = None
            return
        self.start()
    
    def run(self):
        self._runn = True
        self._inn = True
        while self._runn:
            try:
                self.read()
            except Exception as e:
                self.close('disconnect\ne=python exception: {0}\n\n'.format(e.args[0]))
                self._runn = False
                break
            time.sleep(.05)
        self._inn = False
        
    def connected(self):
        # All this really does is check self.sock...
        open = bool(self.sock)
        if not open:
            self._runn = False
        return open
    
    def read(self):
        """Read packets from the socket stream, and store them in self.packet."""
        if not self.connected():
            self._runn = False
            return
        try:
            self._lock.acquire()
            data = self.sock.recv(8192)
            self._lock.release()
        except socket.error as e:
            self._lock.release()
            if e.args[0] == 'timed out':
                return
            if e.args[0] == errno.EAGAIN or (os.name == 'nt' and e.args[0] == errno.WSAEWOULDBLOCK):
                return
            if e.args[0] == errno.EINTR:
                return
            elif self.sock and e.args[0]:
                self.close('disconnect\ne=socket exception: {0}\n\n'.format(e.args[0]))
                return
        data = data.decode(self._charset, 'ignore')
        if not data and self.connected():
            self.close('disconnect\ne=socket closed\n\n')
            return
        self._lock.acquire()
        self.__buffer+= data
        data = self.__buffer.split("\0")
        self.__buffer = data.pop()
        self.packet.extend(data)
        pong = 'ping\n' in self.packet
        self._lock.release()
        if pong:
            self.send('pong\n')
            if self._debug:
                sys.stdout.write('>> Ping!')
    
    def close(self, packet=None):
        try: self.sock.close()
        except socket.error: pass
        self.sock = None
        if packet:
            self.packet.append(packet)
        self._runn = False
    
    def send(self, data):
        if not self.connected(): return
        try:
            self._lock.acquire()
            sent = self.sock.send((data+'\0').encode(self._charset, 'ignore'))
            self._lock.release()
            return sent
        except socket.error:
            return 0
    
    def get_packet(self):
        self._lock.acquire()
        val = False if len(self.packet) == 0 else self.packet.pop(0)
        self._lock.release()
        return val
    
    def get_packets(self):
        self._lock.acquire()
        L = len(self.packet)
        rets = [self.packet.pop(0) for i in range(0, L)]
        self._lock.release()
        return rets
    
    def append(self, pkt):
        self._lock.acquire()
        self.packet.append(pkt)
        self._lock.release()

# EOF
