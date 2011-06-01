''' Example of a very basic dAmn bot!
    Created by photofroggy
'''

import sys

from twisted.internet import reactor

from dAmnViper.base import dAmnSock

# lol
from dAmnViper.examples.util import get_input

# Extend the dAmnViper.dAmnSock class to add some functionality.

class MyClient(dAmnSock):
    
    def init(self, username, password, admin, trigger='!', autojoin=None, callbacks=None):
        self.user.username = username
        self.user.password = password
        self._admin = admin.lower()
        self.trigger = trigger
        self.autojoin = autojoin if bool(autojoin) else ['Botdom']
        self.callbacks = callbacks if bool(callbacks) else {}
    
    def pkt_recv_msg(self, data):
        # Provide basic command firing.
        if data['message'][:len(self.trigger)] == self.trigger:
            data['message'] = data['message'][len(self.trigger):]
            data['args'] = data['message'].split(' ')
            self.callbacks.get(data['args'][0].lower(), self._no_cmd)(data, self)
    
    def _no_cmd(self, data, client):
        pass
    
def cmd_about(data, dAmn):
    """Basic command callback."""
    dAmn.say(data['ns'], data['user']+': Basic dAmn Viper bot by photofroggy.')

def cmd_quit(data, dAmn):
    """Quit command! Enter the admin name in place of 'admin'!"""
    if data['user'].lower() != dAmn._admin:
        return
    dAmn.say(data['ns'], data['user']+': Closing down!')
    dAmn.flag.quitting = True
    dAmn.disconnect()

def cmd_refresh(data, dAmn):
    """Quit command! Enter the admin name in place of 'admin'!"""
    if data['user'].lower() != dAmn._admin:
        return
    dAmn.say(data['ns'], data['user']+': Refreshing connection!')
    dAmn.flag.disconnecting = True
    dAmn.disconnect()
    
if __name__ == '__main__':
    # Create a client
    sys.stdout.write('>> This is an example bot created with dAmn Viper.\n')
    sys.stdout.write('>> Enter the following details to run the example...\n')
    un = get_input('>> Username: ')
    pw = get_input('>> Password: ')
    ad = get_input('>> Admin: ')
    tr = get_input('>> Trigger: ')
    aj = [room.strip() for room in get_input('>> Autojoin: ', True).split(',')]
    while '' in aj:
        aj.remove('')
    aj = aj or ['Botdom']
    sys.stdout.flush()
    dAmn = MyClient(
        un, pw, ad, tr, aj,
        {'about': cmd_about, 'quit': cmd_quit, 'refresh': cmd_refresh}
    )
    sys.stdout.write('>> Starting the client...\n')
    sys.stdout.flush()
    # Start the dAmn client.
    dAmn.start()
    # Start twisted
    reactor.run()

# EOF
