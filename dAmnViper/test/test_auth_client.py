''' dAmnViper.test.test_auth_client module
    Created by photofroggy
    
    This module provides unit tests for testing the oAuthClient object found
    in dAmnViper.dA.oauth.
'''


import os
import sys
import subprocess

from twisted.trial import unittest
from twisted.internet import reactor

from dAmnViper.dA.oauth import oAuthClient
from dAmnViper.test.dummy import oauth


class TestOAuthClient(unittest.TestCase):
    """ Unit tests for the oAuthClient object. """
    
    server = None
    proc = None
    
    def test_invalid_request(self):
        """ Test what happens when an invalid request is sent to the server. """
        
        def onSuccess(request):
            self.fail('Invalid request seen as valid')
        
        def onFailure(err):
            pass
        
        self.server = oAuthClient(reactor)
        self.d = self.server.serve()
        self.d.addCallbacks(onSuccess, onFailure)
        
        # Web request
        self.server.gotResponse(oauth.Request())
        
        return self.d
    
    def test_valid_request(self):
        """ Test what happens when an valid request is sent to the server. """
        
        def onSuccess(request):
            pass
        
        def onFailure(request):
            self.fail('Valid request seen as invalid')
        
        self.server = oAuthClient(reactor)
        self.d = self.server.serve()
        self.d.addCallbacks(onSuccess, onFailure)
        
        # Web request
        self.server.gotResponse(oauth.Request(path='', args={'code':['2376343']}))
        
        return self.d


# EOF