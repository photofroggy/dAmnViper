''' dAmnViper.test.test_protocol_parser module
    Created by photofroggy
    
    This module provides unit tests for testing the protocol parser found in
    dAmnViper.parse.
'''

from twisted.trial import unittest

from dAmnViper.parse import Packet
from dAmnViper.parse import ProtocolParser


class TestProtocolParser(unittest.TestCase):
    """ Unit tests for the protocol parser. """
    
    def setUp(self):
        self.parser = ProtocolParser()
        
    def test_evt_namespace(self):
        """ Test the ``evt_namespace`` method of the protocol parser. """
        # Basic part packet
        packet = Packet('recv chat:Botdom\n\npart photofroggy\nr=timed out')
        
        # evt_namespace should return `recv_part` in this case!
        packet_name = self.parser.evt_namespace(packet)
        
        self.failIf(packet_name != 'recv_part',
            'Protocol parser does not properly determine packet names')
    
    def test_evt_namespace_unknown(self):
        """ Make sure the parser returns a correct value for an unknown packet. """
        # Unsupported packet.
        packet = Packet('foo bar\n')
        
        # evt_namespace should return `unknown` in this case!
        packet_name = self.parser.evt_namespace(packet)
        
        self.failIf(packet_name != 'unknown',
            'Protocol recognised an unsupported packet as a supported packet')
    
    def test_mapper(self):
        """ Test the ``mapper`` method of the protocol parser. """
        # Testing the mapper using a recv_msg packet has the side-effect
        # of testing both the generic_recv and sort methods.
        packet = Packet('recv chat:Botdom\n\nmsg main\nfrom=photofroggy\n\nStupid message here.')
        data = self.parser.mapper(packet)
        
        ''' Time to make sure we got the right data out of the protocol parser.
            The data returned should look like this:
                
                data = {
                    'event': 'recv_msg',
                    'args': {
                        'ns': 'chat:Botdom',
                        'user': 'photofroggy',
                        'message': 'Stupid message here.',
                        'raw': 'recv chat:Botdom\n\nmsg main\nfrom=photofroggy\n\nStupid message here.'
                    },
                    'rules': [
                        ('ns', 'chat:Botdom'),
                        ('user', 'photofroggy'),
                        ('message', 'Stupid message here.'),
                        ('raw', 'recv chat:Botdom\n\nmsg main\nfrom=photofroggy\n\nStupid message here.')
                    ]
                }
            
            There is always an entry in the 'args' dictionary for every tuple
            in 'rules', so for every tuple in 'rules', we know that the
            corresponding 'args' key-value pair exists. This could make testing
            easier, but it's trivial to test both.
        '''
        expected = [
            ('ns', 'chat:Botdom'),
            ('user', 'photofroggy'),
            ('message', 'Stupid message here.'),
            ('raw', 'recv chat:Botdom\n\nmsg main\nfrom=photofroggy\n\nStupid message here.')
        ]
        
        for rule in expected:
            self.failIf(not rule in data['rules'],
                'Protocol parser failed to store {0} value in rules tuple'.format(rule[0]))
            
            self.failIf(not rule[0] in data['args'].keys(),
                'Protocol parser stored no args dictionary entry for the {0} value'.format(rule[0]))
            
            self.failIf(rule[1] != data['args'][rule[0]],
                'Protocol parser stored an incorrect {0} value in the args dictionary'.format(rule[0]))
    
    def test_message_generating(self):
        """ Test the ``logger`` method to make sure it generates messages properly. """
        packet = Packet('recv chat:Botdom\n\nmsg main\nfrom=photofroggy\n\nStupid message here.')
        data = self.parser.mapper(packet)
        
        log_list = self.parser.logger(data['event'], data['rules'], '#Botdom', packet.raw)
        
        self.failIf(log_list is None,
            'Protocol parser did not recognise the given packet')
        
        self.failIf(log_list[0] != '<photofroggy> Stupid message here.',
            'The logger method did not render the correct log message')
        
        self.failIf(log_list[1] != '#Botdom',
            'The logger method returned with the wrong channel namespace')
        
        self.failIf(not log_list[2],
            'The logger method returned with the wrong value for `showns`')
        
        self.failIf(log_list[3],
            'The logger method returned with the wrong value for `mute`')
        
        self.failIf(log_list[4] != 'recv chat:Botdom\n\nmsg main\nfrom=photofroggy\n\nStupid message here.',
            'The logger method did not return the raw packet')


# EOF