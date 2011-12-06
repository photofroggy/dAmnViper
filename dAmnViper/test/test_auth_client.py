''' dAmnViper.test.test_auth_client module
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This module provides unit tests for testing the oAuthClient object found
    in dAmnViper.dA.oauth.
'''


import os
import sys
import time
import subprocess

from twisted.trial import unittest
from twisted.internet import reactor

from dAmnViper.dA.oauth import oAuthClient


class TestOAuthClient(unittest.TestCase):
    """ Unit tests for the oAuthClient object. """
    
    def test_handle_request(self):
        """ Test what happens when a request is sent to the server. """
        
        def onSuccess(request):
            pass
        
        def onFailure(err):
            pass
        
        self.server = oAuthClient(reactor)
        self.d = self.server.serve()
        self.d.addCallbacks(onSuccess, onFailure)
        
        # Web request
        self.server.deferred(None, {})
        
        return self.d


# EOF