''' Authtoken grabbing example.
    Created by photofroggy
    
    This is a basic example of how to get an authtoken using dAmn Viper!
    It also acts as an interactive authtoken grabber when run as a
    script, sort of.
'''

import sys
from twisted.internet import defer

from dAmnViper.base import dAmnSock
from dAmnViper.deviantART import Login

# lol
from dAmnViper.examples.util import get_input

def get_authtoken(un='username', pw='password'):
    clientstr = 'Authtoken Grabber/1 (Python) dAmn Viper/' + dAmnSock.platform.stamp
    login_done(Login(un, pw, client=clientstr))


def login_done(session):
    if session.token is None:
        sys.stdout.write('>> {0}\n'.format(session.status[1]))
    else:
        sys.stdout.write('>> Token: {0}\n'.format(session.token))
    sys.stdout.flush()


if __name__ == '__main__':
    un = get_input('>> Username: ')
    pw = get_input('>> Password: ')
    get_authtoken(un, pw)

# EOF
