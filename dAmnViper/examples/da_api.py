''' Example usage of deviantart API objects.
    Created by photofroggy.
'''

import os
import sys
import time
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
        d.addCallbacks(self.authResponse, self.authFailure)
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
    
    def authResponse(self, response):
        """ Called when the app is successfully authorized. """
        if not response['status']:
            resp = response['data']
            if 'error' in resp.args:
                sys.stdout.write('>> Auth failed: {0}\n'.format(resp.args['error_description'][0]))
            else:
                sys.stdout.write('>> Authorization failed.\n')
                sys.stdout.write('>> Printing debug data...\n')
                sys.stdout.write('>> {0}\n'.format(response['data']))
            self._reactor.stop()
            return response
            
        sys.stdout.write('>> Got auth code!\n')
        # sys.stdout.write('>> debug:\n')
        # sys.stdout.write('>> {0}\n'.format(response.args))
        
        d = self.api.grant(req_state=self.state)
        d.addCallbacks(self.grantResponse, self.grantFailure)
        return response
    
    def authFailure(self, err):
        """ Called when authorization fails. """
        sys.stdout.write('>> Authorization failed.\n')
        sys.stdout.write('>> Printing debug data...\n')
        sys.stdout.write('>> {0}\n'.format(err))
        self._reactor.stop()
        return err
    
    def grantResponse(self, response):
        """ Called when the app is granted access to the API. """
        if not response['status']:
            sys.stdout.write('>> Failed to get an access token.\n')
            
            try:
                sys.stdout.write('>> {0}\n'.format(response['data'].data['error_description']))
            except KeyError:
                pass
            
            self._reactor.stop()
            return
            
        sys.stdout.write('>> Got an access token!\n')
        sys.stdout.write('>> Getting user information...\n')
        # whoami?
        self.api.user_whoami().addCallback(self.whoami)
        return response
    
    def grantFailure(self, response):
        """ Called when the app is refused access to the API. """
        sys.stdout.write('>> Failed to get an access token.\n')
        sys.stdout.write('>> Printing debug data...\n')
        sys.stdout.write('>> {0}\n'.format(response))
        self._reactor.stop()
        return response
    
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
        
        return response
    
    def damntoken(self, response):
        """ Handle the response to whoami API call. """
        
        if response.data is None or 'error' in response.data:
            sys.stdout.write('>> damntoken failed.\n')
            
            try:
                sys.stdout.write('>> {0}\n.'.format(response.data['error_description']))
            except KeyError:
                pass
            
            self._reactor.stop()
            return
        
        sys.stdout.write('>> Authtoken: {0}\n>>\n'.format(response.data['damntoken']))
        sys.stdout.write('>> Refreshing...\n')
        
        d = self.api.refresh(req_state=self.state)
        d.addCallbacks(self.refreshResponse, self.grantFailure)
    
    def refreshResponse(self, response):
        """ Handle the response to the refresh API call. """
        self._reactor.stop()
        if response['status']:
            sys.stdout.write('>> Refresh successful!\n')
            return response
        
        sys.stdout.write('>> Refresh failed: {0}\n'.format(response['data'].data['error_description']))
        return response


if __name__ == '__main__':
    
    app = MyApplication(reactor,
        'id',
        'secret'
    )
    
    app.start('http://localhost:8080')
    
    reactor.run()


# EOF
