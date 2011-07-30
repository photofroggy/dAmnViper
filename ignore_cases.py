''' Ignore cases.
    
    Determine which classes to ignore.
'''

def setup(app):
    app.connect('autodoc-skip-member', ignore_case)

def ignore_case(app, what, name, obj, skip, options):
    if name in ['platform', 'user', 'flag', 'CONST', 'session', 'connection', 'defer']:
        return True
    
    if name.startswith('__'):
        return True
    
    if hasattr(obj, '__doc__') and obj.__doc__ == None:
        return True
    
    return False


# EOF
