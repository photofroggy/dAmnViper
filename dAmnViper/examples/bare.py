''' Example of a client using dAmn Viper's ReconnectingClient class!
    Created by photofroggy
'''

from dAmnViper.base import dAmnSock

if __name__ == '__main__':
    dAmn = dAmnSock()
    dAmn.user.username = 'username'
    dAmn.user.password = 'password'
    dAmn.autojoin = ['Botdom']
    dAmn.start()

# EOF
