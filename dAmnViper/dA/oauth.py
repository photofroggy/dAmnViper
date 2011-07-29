''' dAmnViper.dA.oauth module
    Created by photofroggy.
    
    This module provides objects which can be used to authorize applications
    with deviantart.com's oAuth API. Note that this product is in no way
    affiliated with or endorsed by deviantART.com. This is not an official
    service of deviantART.com. This is an independent project created by
    photofroggy.
'''

from urllib import urlencode

from twisted.web import server
from twisted.web import resource
from twisted.internet import defer


def auth_url(self, client_id, client_secret, response_type='code', **kwargs):
    """ Generate an oAuth url.
        
        Generate a URL for users to visit so they can authorize your
        application with deviantart.com.
    """
    
    kwargs['client_id'] = client_id
    kwargs['client_secret'] = client_secret
    kwargs['response_type'] = response_type
    
    return 'https://www.deviantart.com/oauth2/draft15/authorize?{0}'.format(
        urlencode(kwargs))


class oAuthClient(object):
    """ oAuth client object. """
    resource = AuthResource
    
    def __init__(self, _reactor, port=8080):
        # Store input
        self._reactor = _reactor
        self.d = None
        self.port = port
        self.state = state
        self.agent = agent
    
    def serve(self):
        """ Start serving our oAuth response stuff. """
        self.d = defer.Deferred()
        d = defer.Deferred()
        d.addCallback(self.gotResponse)
        site = server.Site(self.resource(self, d))
        self.sitePort = self._reactor.listenTCP(self.port, site)
        return self.d
    
    def gotResponse(self, request):
        """ Process the response from dA. """
        self.sitePort.stopListening()
        
        if 'code' in request.args:
            self.d.callback(request)
            self.d = None
            return
        
        self.d.errback(request)
        self.d = None


class AuthResource(resource.Resource):
    """ Authorize resource.
        
        This is the object which processes requests sent to localhost.
        Required for processing the response from deviantART when
        requesting an authorization code.
        
        This class is used by the ``oAuthClient`` object.
    """
    
    isLeaf=True
    
    def __init__(self, deferred):
        self.d = deferred
    
    def render_GET(self, request):
        """ Determine whether or not to pass the request to the application. """
        if 'favicon' in request.path:
            return ''
        
        data = request.args or None
        
        if data is None:
            return ''
        
        self.d.callback(request)
        return 'Thanks! You can close this window now!'


# EOF
