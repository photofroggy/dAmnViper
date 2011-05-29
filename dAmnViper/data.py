''' dAmnViper.data module
    This module is part of the dAmnViper package.
    Created by photofroggy.
'''

from dAmnViper.parse import Packet

class Channel:
    """ Objects representing dAmn channels.
        Information about the channels are stored in here.
    """
    
    class header:
        def __init__(self):
            self.content = ''
            self.by = ''
            self.ts = 0.0
    
    def __init__(self, namespace, shorthand):
        """Set up all our variables."""
        self.title = Channel.header()
        self.topic = Channel.header()
        self.pc = {}
        self.pc_order = []
        self.member = {}
        
        self.namespace = namespace
        self.shorthand = shorthand
        
        self.type = '<dAmn channel \''+self.namespace+'\'>'
    
    def process_property(self, data):
        if data['p'] == 'title':
            self.title.content = data['value']
            self.title.by = data['by']
            self.title.ts = data['ts']
        if data['p'] == 'topic':
            self.topic.content = data['value']
            self.topic.by = data['by']
            self.topic.ts = data['ts']
        if data['p'] == 'privclasses':
            self.pc = Packet(data['value'], ':').args
            self.pc_order = sorted(self.pc.keys(), key=int)
            self.pc_order.reverse()
        if data['p'] == 'members':
            member = Packet(data['value'])
            while member.cmd != None and len(member.args) > 0:
                self.register_user(member)
                member = Packet(member.body)
    
    def register_user(self, info, user = None):
        user = user if user != None else info.param
        if user in self.member:
            self.member[user]['con']+= 1
        else:
            self.member[user] = info.args
            self.member[user]['con'] = 1
    
    def __str__(self):
        return self.namespace

# EOF