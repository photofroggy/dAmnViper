''' dAmnViper.test.test_dapi_response module
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This module provides unit tests for testing the Response object found in
    dAmnViper.dA.api.
'''


import sys
import time
import os.path
import subprocess

from twisted.trial import unittest
from twisted.internet import defer
from twisted.internet import reactor

from dAmnViper.dA.api import Request


class TestRequest(unittest.TestCase):
    """ Unit tests for the Request obejct. """
    
    delayed = None
    proc = None
    
    def setUp(self):
        self.proc = subprocess.Popen([
            sys.executable,
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), 'dummy/dapi.py')
            )
        ])
        time.sleep(2)
    
    def test_request(self):
        """ See what happens when we try and send a request. """
        
        def onSuccess(response):
            self.delayed.cancel()
            self.proc.terminate()
            self.failIf(not 'username' in response.data,
                'Failed to process response properly')
        
        def timeout(obj):
            self.fail('No response received')
            self.proc.terminate()
        
        d = defer.Deferred()
        d.addCallback(onSuccess)
        
        self.delayed = reactor.callLater(2, timeout)
        
        req = Request(reactor, d, 'http://localhost:8080/user/whoami')
        
        return d


# EOF
