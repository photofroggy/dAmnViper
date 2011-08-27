''' dAmnViper.test.test_client_connection module
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This module provides unit tests for testing if the Client object is able
    to connect to chat servers properly.
'''

import sys
import os.path
import subprocess

from twisted.trial import unittest
from twisted.internet import defer

from dAmnViper.test.dummy.client import DummyClient


class TestClientConnection(unittest.TestCase):
    """ Test client connection code. Or whatever. """
    
    def test_connecting(self):
        """ Yep. """
        # Start dummy server!
        self.proc = subprocess.Popen([
            sys.executable,
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), 'dummy/server.py')
            )
        ])
        
        # Make a client or something idk.
        self.client = DummyClient()
        self.client.teardown = self._fail
        self.client.pkt_dAmnServer = self._success
        # Configure it.
        self.client.user.username = 'test'
        self.client.user.token = 'dummy'
        
        # Deferred callback and whatnot
        def callback(obj):
            self.client.close()
            self.proc.terminate()
        
        def errback(obj):
            self.proc.terminate()
            self.fail('Failed to connect to the dummy server and handshake.')
        
        self.d = defer.Deferred()
        self.d.addCallbacks(callback, errback)
        
        self.client.start()
        
        return self.d
        
    def _success(self, data):
        """ Called when we have connected! Yay! """
        self.d.callback({})
    
    def _fail(self):
        self.d.errback({})


# EOF