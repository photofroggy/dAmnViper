''' dAmnViper.deviantART module
    Created by photofroggy.
    
    This module provides a method to attempt to grab an authtoken from
    deviantART. Depends on _auth3 or _auth26 depending on which
    version of Python is being used.
    
    The Twisted implementation of dAmnViper cannot be used on Python 3
    until twisted supports Python 3, so _auth3 is redundant in this
    case. However, both files may become redundant if deviantART
    implements the password grant type in their OAuth API.
        
    The nature of the code here means that output to stdout is blocked
    until the request has completed. This may also change when the
    password is available.
'''

import os
import re

_pyver = float(os.sys.version[:3])
if _pyver >= 2.6 and _pyver < 3:
    from dAmnViper._auth26 import fetch_cookie
    from dAmnViper._auth26 import fetch_channel
elif _pyver >= 3:
    from dAmnViper._auth3 import fetch_cookie
    from dAmnViper._auth3 import fetch_channel
else:
    import sys
    sys.stdout.write('>>> Your Python install must be at least Python 2.6!\n')
    sys.stdout.write('>>> Python 3.1 is preferable.\n')
    sys.stdout.flush()
    sys.exit(1)


''' This stuff is stupid holmes.
    Will rewrite this module when CookieAgent is in twisted's releases.

from threading import Thread

def login(reactor, deferred, username, password, extras={'remember_me':'1'}, client='dAmnViper (python 3.x) TokenGrabber/2'):
    """ Creates a subthread which invokes the Login object and passes
        it to the given deferred.
    """
    Thread(target=run_login,
        args=(reactor, deferred, username, password, extras, client)).start()

    
def run_login(reactor, deferred, username, password, extras={'remember_me':'1'}, client='dAmnViper (python 3.x) TokenGrabber/2'):
    """ Invokes the Login object to retrieve an authtoken.
        The resulting object is given to the given deferred.
    """
    reactor.callFromThread(deferred.callback, Login(username, password, extras, client))

'''

class Login:
    """ Login session object.
        
        Instances of this class represent a login session for deviantART.
        The object uses the data given in the constructor to try and
        log in to deviantART and retrieve and authtoken for the
        chatrooms.
        
        As an example, the following code may be used::
            
            session = Login('username', 'password')
        
        After the ``Login`` object has finished running, ``status`` can
        have one of the following values::
            
            # If we got an authtoken.
            session.status = (1, 'Authtoken retrieved!')
            
            # If we didn't get an authtoken but don't know why.
            session.status = (2, 'Authtoken not given. Not sure why.')
            
            # If we could not connect to the internet.
            session.status = (3, 'Could not connect to the internet.')
            
            # If the login details were incorrect.
            session.status = (4, 'Incorrect username or password provided.')
            
            # If there was a problem with the request.
            self.status = (5, request_error_message)
            
            # If the account we're trying to use is not verified.
            session.status = (6,
                "This account has not yet been verified. To verify, please check the email you used to register the account (don't forget to search junk mail), and click the link the email deviantART sent you.")
            
            # If everything failed but we can't figure out why.
            session.status = (7, 'Something went wrong. I do not know why.')
        
        Assuming that the login attempt succeeded, the dAmn authtoken is
        stored in the ``token`` attribute. The ``jar`` attribute stores
        the cookie jar used during the login process.
    """
    
    url = 'https://www.deviantart.com/users/login'
    curl = 'http://chat.deviantart.com/chat/botdom'
    
    def __init__(self, username, password, extras={'remember_me':'1'}, client='dAmnViper (python 3.x) TokenGrabber/2'):
        """ Initialise the object. Fetch and process an authtoken. """
        self.jar = None
        self.cookie = None
        self.token = None
        self.response = None
        self.status = (0, 'Nothing has happened yet.')
        # Attempt to fetch the authoken!
        response = fetch_cookie(self, username, password, extras, client)
        # Process the response!
        if not self.valid_login_url(response):
            self.handle(response)
            return
        response = fetch_channel(self, self.curl, client)
        # Process the response!
        url = response.geturl()
        if url == 'ConnectionError' or url != self.curl:
            self.handle(response)
            return
        self.crop(username, response.data)
    
    def valid_login_url(self, response):
        """ Check the URL we are redirected to after trying to log in. """
        url = response.geturl()
        if url == 'ConenctionError':
            return False
        if 'wrong-password' in url:
            return False
        if 'verify.deviantart.com' in url:
            return False
        return True
    
    def crop(self, username, data):
        """ Try to crop the authtoken from the retrieved chat page. """
        match = re.search('"'+username+'", "([0-9a-f]{32})"', data, re.IGNORECASE)
        if match is None or match.group(1) is None:
            self.status = (2, 'Authtoken not given. Not sure why.')
            return
        self.token = match.group(1)
        self.status = (1, 'Authtoken retrieved!')
    
    def handle(self, response):
        """ Try and determine why the login attempt failed. """
        loc = response.geturl()
        if 'verify.deviantart.com' in loc:
            self.status = (6,
                "This account has not yet been verified. To verify, please check the email you used to register the account (don't forget to search junk mail), and click the link the email deviantART sent you.")
            return
        if 'wrong-password' in loc:
            self.status = (4, 'Incorrect username or password provided.')
            return
        if loc in ('localhost', 'ConnectionError'):
            status = response.headers.get('Status')
            if status[0] == -2:
                self.status = (3, 'Could not connect to the internet.')
            else:
                self.status = (5, status[1])
            return
        self.status = (7, 'Something went wrong. I do not know why.')

# EOF
