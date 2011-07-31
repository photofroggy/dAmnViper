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


from dAmnViper.dA.oauth import oAuthClient


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
        self.raw_data = data
        
        try:
            self.data = json.loads(str(data))
        except Exception as e:
            self.data = None


class Request(object):
    """ Send an API request.
        
        This is a helper object to send requests to API methods.
        
        Gives response data to the callback given to the contructor.
    """
    
    def __init__(self, _reactor, deferred, url, agent='dAmnViper/dA/api/request', response=None):
        self._reactor = _reactor
        self.d = deferred
        self.agent = agent
        self.url = url
        self.agent = agent
        self.response_obj = response
        
        if self.response_obj is None:
            self.response_obj = Response
        
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
        self.d.callback(self.response_obj(self.response, data))


class APIClient(object):
    """ Client for deviantart.com's API. """
    
    def __init__(self, _reactor, client_id, client_secret, auth_code=None, token=None, agent='dAmnViper/dA/api/apiclient'):
        self._reactor = _reactor
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_code = auth_code
        self.token = token
        self.agent = agent
        # Auth deferred
        self._authd = None
        self._grantd = None
        # URL stuff
        self.draft = 'draft15'
        self.api_url = 'https://www.deviantart.com/'
        # Custom? Maybe
        self.init()
    
    def init(self):
        """ Override this method if you want to customise the class a bit. """
        pass
    
    def auth_app(self, port=8080, resource=None, html=None):
        """ Start the oAuth client. """
        client = oAuthClient(self._reactor, port, resource, html)
        # Start serving requests.
        d = client.serve()
        # Defer the handling or whatever.
        d.addCallbacks(self._authResponse, self._authResponse)
        # Make a deferred to be used externally.
        self._authd = defer.Deferred()
        return self._authd
    
    def _authResponse(self, response):
        """ Process the response from deviantart. """
        if 'code' in response.args:
            self.auth_code = response.args['code'][0]
            self._authd.callback(response)
            return
        
        self._authd.errback(response)
    
    def url(self, klass, method=None, api='api', **kwargs):
        """ Create an API URL based on the input. """
        args = {}
        
        for key, value in kwargs.iteritems():
            if not value:
                continue
            args[key] = value
        
        return '{0}{1}/{2}/{3}{4}{5}'.format(self.api_url, api, self.draft, klass,
            '' if method is None else '/{0}'.format(method),
            '' if not args else '?{0}'.format(urlencode(args)))
    
    def requiresToken(self):
        """ If the token is not set, raise a ``ValueError``. """
        if self.token is None:
            raise ValueError('token required for this method')
    
    def makeRequest(self, url, response_obj=None):
        """ Send a request to the api. """
        d = defer.Deferred()
        Request(self._reactor, d, url, self.agent, response_obj)
        return d
    
    def grant(self, auth_code=None, req_state=None):
        """ Request a grant token. """
        if auth_code != None:
            self.auth_code = auth_code
        
        if self.auth_code is None:
            raise ValueError('Authorization code must not be None')
        
        d = self.makeRequest(self.url('token', api='oauth2',
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type='authorization_code',
            state=req_state,
            code=self.auth_code
        ))
        d.addCallbacks(self.handle_grant, self.handle_grant_fail)
        self._grantd = defer.Deferred()
        
        return self._grantd
    
    def handle_grant(self, response):
        """ Handle the response to the grant api call. """
        if response.data is not None and response.data['status'] == 'success':
            self.token = response.data['access_token']
            self._grantd.callback(response)
            return
        
        self._grantd.errback(response)
    
    def handle_grant_fail(self, err):
        sefl._grantd.errback(err)
    
    def placebo(self, token=None):
        """ Check that the access token is still valid. """
        if token != None:
            self.token = token
        else:
            self.requiresToken()
        
        return self.makeRequest(self.url('placebo', access_token=self.token))
    
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
