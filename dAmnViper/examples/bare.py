''' Example of a client using dAmn Viper's dAmnSock class!
    Created by photofroggy
'''

from twisted.internet import reactor

from dAmnViper.base import dAmnSock

if __name__ == '__main__':
    
    dAmn = dAmnSock()
    
    dAmn.user.username = 'username'
    dAmn.user.password = 'password'
    dAmn.autojoin = ['Botdom']
    
    dAmn.teardown = lambda: reactor.stop()
    
    dAmn.start()
    
    if dAmn.flag.connecting:
        reactor.run()

# EOF
