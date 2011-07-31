''' dAmnViper.test.dummy.client module
    Created by photofroggy
    
    This module provides a dummy client which can be used to test the
    connectivity of the Client class. The DummyClient object here is similar
    to the dAmnClient object provided in dAmnViper.base.
'''

from dAmnViper.base import ChatClient

class DummyClient(ChatClient):
    """ Dummy chat client. """

    def init(self, *args, **kwargs):
        """ Initiate everything. """
        # Populate our attributes.
        self.agent = 'dAmnViper/test/dummy/client'
        self.connection.limit = 0
        # Configure the class to connect to the dAmn server.
        self.CONST.SERVER = 'localhost'
        self.CONST.CLIENT = 'dAmnClient 0.3'
        self.CONST.PORT = 8000
        # Make the client less noisy for the test.
        self.stdout = lambda n: None
    
    def startedConnecting(self, connector):
        """ This method is called when we have started connecting. """
        self.logger('** Opening connection to dAmn...', showns=False)
        self.flag.connecting = True
        self.on_connection_start(connector)


# EOF