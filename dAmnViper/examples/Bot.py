''' Example of a very basic dAmn bot!
    Created by photofroggy
'''

from dAmnViper.base import ReconnectingClient

# Extend the dAmnViper.ReconnectingClient class to add some functionality.

class my_client(ReconnectingClient):
    
    def __inst__(self, username, password, admin, trigger='!', autojoin=None, callbacks=None):
        ReconnectingClient.__inst__(self) # Useful to call this.
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
    dAmn = my_client(
        'username', 'password', 'admin', '!',
        ['Botdom'], {'about': cmd_about, 'quit': cmd_quit, 'refresh': cmd_refresh}
    )
    # Start the dAmn client.
    dAmn.start()

# EOF
