''' dAmnViper.test.test_packet_event_object module
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This module provides unit tests for testing the packet event object found
    in dAmnViper.parse.
'''

from twisted.trial import unittest

from dAmnViper.parse import PacketEvent


class TestPacketEventObject(unittest.TestCase):
    """ Unit tests for the PacketEvent object. """
    
    def test_store_event_name(self):
        """ Test whether the object actually keeps record of the event name. """
        pevent = PacketEvent('recv_msg')
        
        self.failIf(pevent.name != 'recv_msg', 'Failed to store packet event name')
    
    def test_access_argument(self):
        """ Test whether or not arguments can be accessed by name. """
        pevent = PacketEvent('recv_msg', [('user', 'photofroggy')])
        
        try:
            user = pevent('user')
            self.failIf(user != 'photofroggy',
                'Returned wrong value for user argument')
        except KeyError:
            self.fail('Argument not found by `arg` method')
    
    def test_access_invalid(self):
        """ Test accessing an argument which is not stored. """
        pevent = PacketEvent('recv_msg', [('user', 'photofroggy')])
        
        try:
            property = pevent('p')
            self.fail('No error thrown')
        except KeyError:
            return
    
    def test_check_index(self):
        """ Test getting the names of arguments. """
        pevent = PacketEvent('recv_msg', [('user', 'photofroggy')])
        
        self.failIf(not 'user' in pevent.arguments,
            'Failed to get all argument names')


# EOF
