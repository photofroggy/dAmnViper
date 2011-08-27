''' dAmnViper.test.test_dapi_receiver module
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This module provides unit tests for testing the ResponseReceiver object
    found in dAmnViper.dA.api.
'''


from twisted.trial import unittest
from twisted.internet import defer

from dAmnViper.dA.api import ResponseReceiver


class TestResponseReceiver(unittest.TestCase):
    """ Unit tests for the response receiver. """
    
    def test_buffer(self):
        """ Make sure that data is buffered and returned properly. """
        d = defer.Deferred()
        recv = ResponseReceiver(d)
        
        def got_response(response):
            self.failIf(response != 'foobar', 'Unexpected response given')
        
        d.addCallback(got_response)
        
        recv.dataReceived('foo')
        recv.dataReceived('bar')
        recv.connectionLost('reason')


# EOF
