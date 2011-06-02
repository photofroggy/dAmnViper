''' dAmnViper._auth26 module
    created by photofroggy.
    
    This module performs the HTTP requests required for fetching
    authtokens. The code here does not work with Python 3.
'''

import re
import urllib
import urllib2
import cookielib
    
class HTTPResponder:
    headers = {
        'Location': 'localhost',
        'Status': (0, False),
    }
    
    def __init__(self, url, data=''):
        self.url = url
        self.data = data
    
    def geturl(self, *args, **kwargs):
        return self.url

def fetch_cookie(obj, username, password, extras={'remember_me':'1'}, client='dAmnViper (python2.x) TokenGrabber/2'):
    """ Fetch a login cookie from deviantART.com. """
    extras.update({'username': username, 'password': password})
    obj.jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(obj.jar))
    req = urllib2.Request(
        obj.url,
        urllib.urlencode(extras),
        {'User-Agent': client},
    )
    try:
        response = opener.open(req)
    except IOError as e:
        response = HTTPResponder('ConnectionError')
        response.headers['Status'] = (e.reason.errno, e.strerror)
    return response
    # Well, that was nice and easy :D

def fetch_channel(obj, url='http://chat.deviantart.com/chat/botdom', client='dAmnViper (python2.x) TokenGrabber/2'):
    """ Fetch a channel page from deviantART.com. """
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(obj.jar))
    req = urllib2.Request(
        url,
        urllib.urlencode({}),
        {'User-Agent': client})
    response = {}
    try:
        resp = opener.open(req)
        response = HTTPResponder(resp.geturl(), resp.read())
    except IOError as e:
        response = HTTPResponder('ConnectionError')
        response.headers['Status'] = (e.reason.errno, e.strerror)
    return response

# EOF
