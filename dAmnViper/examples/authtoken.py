''' Authtoken grabbing example.
    Created by photofroggy
    
    This is a basic example of how to get an authtoken using dAmn Viper!
    It also acts as an interactive authtoken grabber when run as a
    script, sort of.
'''

from dAmnViper.base import dAmnSock
from dAmnViper.deviantART import Login

def get_authtoken(un='username', pw='password'):
    clientstr = 'Authtoken Grabber/1 (Python/3.0) dAmn Viper/' + dAmnSock.platform.stamp
    session = Login(un, pw, client=clientstr)
    
    if session.token is None:
        print('>>',session.status[1])
    else:
        print('>> Token:',session.token)

if __name__ == '__main__':
    # Designed for use with Python 3.x
    # Change input to raw_input to make it work with earlier versions.
    un = input('>> Username: ').strip()
    pw = input('>> Password: ').strip()
    get_authtoken(un, pw)

# EOF
