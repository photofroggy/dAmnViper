''' dAmnViper.test.dummy.oauth module
    Created by photofroggy
    
    Dummy classes used for testing stuff in the dAmnViper.dA.oauth module.
'''


class Request(object):
    """ Dummy request objected. Very simple stuff. """
    
    def __init__(self, path='/', args={}):
        self.path = path
        self.args = args
        self.flag = False


# EOF
