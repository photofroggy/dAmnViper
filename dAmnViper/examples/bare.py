''' Example of a client using dAmn Viper's dAmnClient class!
    Created by photofroggy
'''

import os
import sys

from twisted.internet import reactor

sys.path.insert(0, os.curdir)

from dAmnViper.base import dAmnClient

if __name__ == '__main__':
    
    dAmn = dAmnClient()
    
    dAmn.user.username = 'username'
    dAmn.user.token = 'authtoken'
    dAmn.autojoin = ['Botdom']
    
    dAmn.teardown = lambda: reactor.stop()
    
    dAmn.start()
    
    if dAmn.flag.connecting:
        reactor.run()

# EOF
