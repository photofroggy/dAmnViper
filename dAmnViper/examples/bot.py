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
        self.autojoin = autojoin or ['Botdom']
        self.callbacks = callbacks or Commands()
    
    def teardown(self):
        reactor.stop()
    
    def pkt_recv_msg(self, data):
        # Provide basic command firing.
        if data['message'][:len(self.trigger)] == self.trigger:
            data['message'] = data['message'][len(self.trigger):]
            data['args'] = data['message'].split(' ')
            self.callbacks.handle(
                data['args'][0].lower(), data, self)


class Commands(object):
    """ Just a simple object to hold any command callbacks. """
    
    def handle(self, cmd, data, client):
        getattr(self, 'cmd_{0}'.format(cmd),
            self.unknown_cmd)(data, client)
    
    def unknown_cmd(self, data, client):
        pass
    
    def cmd_about(self, data, dAmn):
        """Basic command callback."""
        dAmn.say(data['ns'], data['user']+': Basic dAmn Viper bot by photofroggy.')
    
    def cmd_quit(self, data, dAmn):
        """Quit command! Enter the admin name in place of 'admin'!"""
        if data['user'].lower() != dAmn._admin:
            return
        dAmn.say(data['ns'], data['user']+': Closing down!')
        dAmn.flag.quitting = True
        dAmn.disconnect()
    
    def cmd_refresh(self, data, dAmn):
        """Quit command! Enter the admin name in place of 'admin'!"""
        if data['user'].lower() != dAmn._admin:
            return
        dAmn.say(data['ns'], data['user']+': Refreshing connection!')
        dAmn.flag.disconnecting = True
        dAmn.disconnect()
        

def configure():
    sys.stdout.write('>> We need some details to be able to run the bot\n')
    
    obj = [get_input('>> Username: '),
        get_input('>> Password: '),
        get_input('>> Admin: '),
        get_input('>> Trigger: '),
        [room.strip() for room in get_input('>> Autojoin: ', True).split(',')]
    ]
    
    while '' in obj[4]:
        obj[4].remove('')
    obj[4] = obj[4] or ['Botdom']
    
    return obj


if __name__ == '__main__':
    # Create a client
    sys.stdout.write('>> This is an example bot created with dAmn Viper.\n')
    
    dAmn = MyClient(*configure(), callbacks=Commands())
    
    sys.stdout.write('>> Starting the client...\n')
    sys.stdout.flush()
    
    # Start the dAmn client.
    dAmn.start()
    
    if not dAmn.flag.connecting:
        sys.exit()
    
    # Start twisted
    reactor.run()

# EOF
