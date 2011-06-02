''' dAmnViper._auth3 module
    created by photofroggy.
    
    This module performs the HTTP requests required for fetching
    authtokens. The code here does not work with Python 2.
'''

import re
import urllib.parse
import urllib.request
import http.cookiejar
    
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
    
def fetch_cookie(obj, username, password, extras={'remember_me':'1'}, client='dAmnViper (python3.x) TokenGrabber/2'):
    extras.update({'username': username, 'password': password})
    obj.jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(obj.jar))
    req = urllib.request.Request(
        obj.url,
        urllib.parse.urlencode(extras).encode(),
        {'User-Agent': client},
    )
    try:
        response = opener.open(req)
    except IOError as e:
        response = HTTPResponder('ConnectionError')
        response.headers['Status'] = (e.reason.errno, e.strerror)
    return response
    # Well, that was nice and easy :D

def fetch_channel(obj, url='http://chat.deviantart.com/chat/botdom', client='dAmnViper (python3.x) TokenGrabber/2'):
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(obj.jar))
    req = urllib.request.Request(
        url,
        urllib.parse.urlencode({}).encode(),
        {'User-Agent': client})
    response = {}
    try:
        resp = opener.open(req)
        response = HTTPResponder(resp.geturl(), resp.read().decode('latin-1'))
    except IOError as e:
        response = HTTPResponder('ConnectionError')
        response.headers['Status'] = (e.reason.errno, e.strerror)
    return response

# EOF
