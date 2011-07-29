''' dAmnViper.dA.oauth module
    Created by photofroggy.
    
    This module provides objects which can be used to authorize applications
    with deviantart.com's oAuth API. Note that this product is in no way
    affiliated with or endorsed by deviantART.com. This is not an official
    service of deviantART.com. This is an independent project created by
    photofroggy.
'''


import json
from urllib import urlencode

from twisted.web import server
from twisted.web import resource
from twisted.internet import defer
from twisted.internet import protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers


class ResponseReceiver(protocol.Protocol):
    """ Response receiver.
        
        A simple object used to receive responses from a web request.
    """
    
    def __init__(self, deferred):
        self.d = deferred
        self.b = ''
    
    def dataReceived(self, data):
        """ Store any received data in the buffer. """
        self.b+= data
    
    def connectionLost(self, reason):
        """ Make sure we do something with the response. """
        self.d.callback(self.b)


class Response(object):
    """ API Response object. """
    
    def __init__(self, head, data):
        self.head = head
        self.data = json.loads(data)


class Request(object):
    """ Send an API request.
        
        This is a helper object to send requests to API methods.
        
        Gives response data to the callback given to the contructor.
    """
    
    def __init__(self, _reactor, deferred, url, agent='dAmnViper/dA/api/request'):
        self._reactor = _reactor
        self.d = deferred
        self.agent = agent
        self.url = url
        self.agent = agent
        self.start_request()
    
    def start_request(self):
        """ Send the token request to deviantART. """
        agent = Agent(self._reactor)
        d = agent.request('POST', self.url, Headers({'User-Agent': [self.agent]}), None)
        d.addCallback(self.received_response)
    
    def received_response(self, response):
        """ Received a response. Get the response body. """
        self.response = response
        d = defer.Deferred()
        d.addCallback(self.got_data)
        response.deliverBody(ResponseReceiver(d))
    
    def got_data(self, data):
        """ Received when we have the response body. """
        if self.d.callback is None:
            return
        self.d.callback(Response(self.response, data))


class APIClient(object):
    """ Client for deviantart.com's API. """
    
    def __init__(self, _reactor, client_id, client_secret, token=None, agent='dAmnViper/dA/api/apiclient'):
        self._reactor = _reactor
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.agent = agent
        # URL stuff
        self.draft = 'draft15'
        self.api_url = 'https://www.deviantart.com/api/'
        
    def url(self.klass, method=None, **kwargs):
        """ Create an API URL based on the input. """
        args = {}
        
        for key, value in kwargs.iteritems():
            if value is None:
                continue
            args[key] = value
        
        return '{0}{1}/{2}{3}{4}'.format(self.api_url, self.draft, klass,
            '' if method if None else '/{0}'.format(method),
            '' if not args else '?{0}'.format(urlencode(args)))
    
    def requiresToken(self):
        """ If the token is not set, raise a ``ValueError``. """
        if self.token is None:
            raise ValueError('token required for this method')
    
    def makeRequest(self, url):
        """ Send a request to the api. """
        d = defer.Deferred()
        Request(self._reactor, d, url, self.agent)
        return d
    
    def grant(self, auth_code, req_state=None):
        """ Request a grant token. """
        return self.makeRequest(self.url('grant',
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type='authorization_code',
            state=req_state,
            code=auth_code
        ))
    
    def user_whoami(self, token=None):
        """ Request info on the user. """
        if token != None:
            self.token = token
        else:
            self.requiresToken()
        
        return self.makeRequest(self.url('user', 'whoami', access_token=self.token))
    
    def user_damntoken(self, token=None):
        """ Request info on the user. """
        if token != None:
            self.token = token
        else:
            self.requiresToken()
        
        return self.makeRequest(self.url('user', 'damntoken', access_token=self.token))


# EOF
