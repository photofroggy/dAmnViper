==========
dAmn Viper
==========

**dAmn Viper** is a Python package created by photofroggy.

This package provides an API for connecting to and interacting with
the dAmn chats. That is, deviantART's messaging network chats.

This branch of dAmn Viper currently only works with Python 2.6 and up
due to use of the twisted library.

-------------
Brief example
-------------

Creating a client quickly for dAmn is quite easy using dAmn Viper. Below
is one of the simplest examples of a client that simply connects, and
tries to stay connected::
    
    from dAmnViper.base import dAmnSock
    
    dAmn = dAmnSock()
    dAmn.user.username = 'username'
    dAmn.user.password = 'password'
    dAmn.autojoin = ['Botdom']
    dAmn.start()

That is all that is required! It is advised that you use the
ReconnectingClient class when making applications that connect to dAmn.
Chat bots and full clients can be made by extending the
ReconnectingClient class to add functionality, as shown in the examples
provided.

---------
Prospects
---------

This is an experimental branch which uses Twisted for the interactions
between the application and dAmn. I am currently uncertain whether or
not to use this for the master branch as it means end users would have
more dependencies to install when setting up an application that uses
dAmn Viper. This argument is negated if the application is bundled, or
has appropriate installers created.

So far, one major disadvantage of using twisted over the standard
library, is that the loading time is considerably slower under Ubuntu.
This appears to be due to the use of asynchronous methods to retrieve
an authtoken in `dAmnViper.deviantART`. This will be revised when
twisted's own `CookieAgent` class is available in the distributed
copies of twisted.

------------
Dependencies
------------

A further disadvantage is the acquisition of dependencies. This means
that applications using dAmn Viper will depend on twisted as well as
dAmn Viper.

In addition, when the aforementioned `CookieAgent` is available,
applications will also depend on PyOpenSSL. This is not exactly a great
situation for application developers and end users.

It is more of an issue for end users, as they will not want to spend
time installing multiple dependencies. This problem can, however, be
eleminated by creating installers for applications using dAmn Viper.

As such, this is somewhat a non-point, but it does mean an installer
has to be created to achieve easy setup for end users. Fortunately,
installers are something which users tend to be ok at using, so long as
they aren't too complicated. Having an installer which downloads and
installs multiple dependencies may complicate things too much. We'll
see.

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
