''' dAmnViper.test.test_dapi_client module
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This module provides unit tests for testing the APIClient object found in
    dAmnViper.dA.api.
'''


import sys
import time
import os.path
import subprocess

from twisted.trial import unittest
from twisted.internet import defer
from twisted.internet import reactor

from dAmnViper.dA.api import APIClient


class TestAPIClient(unittest.TestCase):
    """ Unit tests for the APIClient object. """
    
    def setUp(self):
        self.client = APIClient(reactor, '9001', 'somesecret')
        self.client.api_url = 'http://localhost:8080/'
    
    def test_generate_url(self):
        """ See if URL generation works properly. """
        url = self.client.url('user', 'whoami')
        
        if url == 'http://localhost:8080/api/draft15/user/whoami':
            return
        
        self.fail('APIClient generated url incorrectly: {0}'.format(url))
    
    def test_request_without_token(self):
        """ Make sure certain requests fail when no token is present. """
        
        try:
            self.client.user_whoami()
        except ValueError:
            return
        
        self.fail('Client sent request without a token')
    
    def test_request_correct(self):
        """ Make sure this succeeds! """
        # dummy server
        self.proc = subprocess.Popen([
            sys.executable,
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), 'dummy/dapi.py')
            )
        ])
        time.sleep(2)
        
        d = self.client.user_whoami(token='23534')
        
        def handle(response):
            self.delayed.cancel()
            self.proc.terminate()
            if response.data is None or not 'username' in response.data:
                self.fail('Failed to process response{0}'.format(
                '' if not response.raw_data else ' from "{0}"'.format(response.raw_data)))
        
        d.addCallback(handle)
        
        def timeout():
            self.proc.terminate()
            self.fail('No response received')
        
        self.delayed = reactor.callLater(10, timeout)
        
        return d


# EOF
