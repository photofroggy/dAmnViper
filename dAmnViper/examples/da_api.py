''' Example usage of deviantart API objects.
    Created by photofroggy.
'''

import os
import sys
from twisted.internet import reactor

sys.path.insert(0, os.curdir)

from dAmnViper.dA import api


class MyApplication(object):
    """ Just an example type thingy. """
    
    def __init__(self, _reactor, id, secret, port=8080, agent='dAmnViper/example/daapiclient', state=None):
        self._reactor = _reactor
        self.id = id
        self.secret = secret
        self.port = port
        self.state = state
        # Set up the API client
        self.api = api.APIClient(_reactor, id, secret, agent=agent)
    
    def start(self, redirect, html=None):
        """ Start the application.
            
            All this really does is start the auth server and then display a
            url on screen. The user should visit this url to authorize the app.
        """
        d = self.api.auth_app(self.port, html)
        d.addCallbacks(self.authSuccess, self.authFailure)
        # Make a url
        url = self.api.url('authorize', api='oauth2',
            client_id=self.id,
            client_secret=self.secret,
            redirect_uri=redirect,
            response_type='code',
            state=self.state
        )
        # Send user there, somehow...
        sys.stdout.write('>> Visit the following URL to authorize this app:\n')
        sys.stdout.write('>> {0}\n'.format(url))
        
        # Now we wait for the user's webbrowser to be redirected to our server.
    
    def authSuccess(self, response):
        """ Called when the app is successfully authorized. """
        sys.stdout.write('>> Got auth code!\n')
        # sys.stdout.write('>> debug:\n')
        # sys.stdout.write('>> {0}\n'.format(response.args))
        
        d = self.api.grant(req_state=self.state)
        d.addCallbacks(self.grantSuccess, self.grantFailure)
    
    def authFailure(self, response):
        """ Called when authorization fails. """
        sys.stdout.write('>> Authorization failed.\n')
        sys.stdout.write('>> Printing debug data...\n')
        sys.stdout.write('>> {0}\n'.format(response))
        self._reactor.stop()
    
    def grantSuccess(self, response):
        """ Called when the app is granted access to the API. """
        sys.stdout.write('>> Got an access token!\n')
        sys.stdout.write('>> Getting user information...\n')
        # whoami?
        self.api.user_whoami().addCallback(self.whoami)
    
    def grantFailure(self, response):
        """ Called when the app is refused access to the API. """
        sys.stdout.write('>> Failed to get an access token.\n')
        sys.stdout.write('>> Printing debug data...\n')
        sys.stdout.write('>> {0}\n'.format(response))
        self._reactor.stop()
    
    def whoami(self, response):
        """ Handle the response to whoami API call. """
        sys.stdout.write('=' * 80)
        sys.stdout.write('\n')
        
        if not 'username' in response.data:
            sys.stdout.write('>> whoami failed.\n')
            # damntoken?
            self.api.user_damntoken().addCallback(self.damntoken)
            return
        
        sys.stdout.write('>> Account: {0}{1}\n'.format(
            response.data['symbol'], response.data['username']))
        
        # damntoken?
        self.api.user_damntoken().addCallback(self.damntoken)
    
    def damntoken(self, response):
        """ Handle the response to whoami API call. """
        self._reactor.stop()
        
        if response.data is None:
            sys.stdout.write('>> damntoken failed.\n')
            return
        
        sys.stdout.write('>> Authtoken: {0}\n'.format(response.data['damntoken']))


if __name__ == '__main__':
    
    app = MyApplication(reactor,
        'client_id',
        'client_secret'
    )
    
    app.start('http://localhost:8080')
    
    reactor.run()


# EOF
