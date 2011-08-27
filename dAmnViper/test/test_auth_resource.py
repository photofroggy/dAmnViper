''' dAmnViper.test.test_auth_resource module
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This module provides unit tests for testing the AuthResource object found
    in dAmnViper.dA.oauth.
'''


from twisted.trial import unittest

from dAmnViper.dA.oauth import AuthResource
from dAmnViper.test.dummy import oauth


class TestAuthResource(unittest.TestCase):
    """ Unit tests for the AuthResource object. """
    
    def test_get_favicon(self):
        """ Test what happens when a favicon is requested. """
        req = oauth.Request(path='favicon.ico')
        
        def failRequest(req):
            self.fail('favicon request was sent to callback')
        
        response = AuthResource(failRequest).render_GET(req)
        
        self.failIf(response != '',
            'favicon request actually returned something')
    
    def test_empty_request(self):
        """ Test what happens when no data is given. """
        req = oauth.Request()
        
        def failRequest(req):
            self.fail('empty request was sent to callback')
        
        response = AuthResource(failRequest).render_GET(req)
        
        self.failIf(response != '',
            'empty request actually returned something')
    
    def test_valid_request(self):
        """ Test what happens when the good stuff is given. """
        req = oauth.Request(args={'code':['something']})
        
        def setFlag(req):
            req.flag = True
        
        response = AuthResource(setFlag).render_GET(req)
        
        self.failIf(not req.flag, 'callback not called for a valid request')
        
        self.failIf(not response, 'empty response given for a valid request')


# EOF
