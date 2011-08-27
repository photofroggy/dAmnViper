''' dAmnViper.test.test_auth_client module
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This module provides unit tests for testing the oAuthClient object found
    in dAmnViper.dA.oauth.
'''


import os
import sys
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
        self.server.gotResponse({})
        
        # There's really no need to return a callback here. ``gotResponse``
        # invokes our callback without waiting. So yeah... Just to be safe,
        # though.
        
        return self.d


# EOF