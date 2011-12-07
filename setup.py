''' dAmnViper setup.
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
'''

from setuptools import setup
import os
import sys
import os.path

sys.path.insert(0, os.path.dirname(__file__))

setup(name='dAmnViper',
    version='3.59',
    description='dAmn connection library',
    author='photofroggy',
    author_email='froggywillneverdie@msn.com',
    url='https://github.com/photofroggy/dAmnViper',
    packages=[
        'dAmnViper',
        'dAmnViper.dA',
        'dAmnViper.examples',
        'dAmnViper.test',
        'dAmnViper.test.dummy'
    ],
    provides=['dAmnViper'],
    requires=['twisted (>=11.0.0)'],
    install_requires=['twisted'],
    platforms=['Any'],
    classifiers=[
        'Natural Language :: English',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    long_description="""
==========
dAmn Viper
==========

**dAmn Viper** is a Python package created by photofroggy.

This package provides an API for connecting to and interacting with the dAmn
chats. That is, deviantART's messaging network chats.

This branch of dAmn Viper is only known to work with Python 2.7 and up due to
use of the twisted library.

-------------
Brief example
-------------

Creating a client quickly for dAmn is quite easy using dAmn Viper. Below
is one of the simplest examples of a client that simply connects, and
tries to stay connected::
    
    from twisted.internet import reactor
    from dAmnViper.base import dAmnClient
    
    dAmn = dAmnClient()
    
    dAmn.user.username = 'username'
    dAmn.user.token = 'authtoken'
    dAmn.autojoin = ['Botdom']
    
    dAmn.on_connection_start = lambda connector: reactor.start()
    dAmn.teardown = lambda: reactor.stop()
    
    dAmn.start()

That is all that is required! It is advised that you use the dAmnClient class
when making applications that connect to dAmn. Chat bots and full clients can
be made by extending the dAmnClient class to add functionality, as shown in the
examples provided.

------------
Dependencies
------------

A disadvantage of using twisted is the acquisition of dependencies. This means
that applications using dAmn Viper will depend on twisted as well as
dAmn Viper.

It is more of an issue for end users, as they will not want to spend
time installing multiple dependencies. This problem can, however, be
eleminated by creating installers for applications using dAmn Viper.

As such, this is somewhat a non-point, but it does mean an installer has to be
created to achieve easy setup for end users. Fortunately, installers are
something which users tend to be ok at using, so long as they aren't too
complicated. Having an installer which downloads and installs multiple
dependencies may complicate things too much. We'll see.

--------
Feedback
--------

Feedback on this branch of dAmn Viper would be very much appreciated.
Please send any feedback to my deviantART account via notes, or submit
something on github, I dunno.

Thanks for reading.

----------
DISCLAIMER
----------

Disclaimer::

		dAmn Viper is in no way affiliated with or endorsed by deviantART.com.
	This is not an official service of deviantART.com. This is an independent
	project created by Henry Rapley:
		<http://photofroggy.deviantart.com>
	
		THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
	APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
	HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
	OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
	THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
	PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
	IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
	ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

"""
)

# EOF
