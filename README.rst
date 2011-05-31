==========
dAmn Viper
==========

**dAmn Viper** is a Python package created by photofroggy.

This package provides an API for connecting to and interacting with
the dAmn chats. That is, deviantART's messaging network chats.

The package was created using Python version 3, so should be used with
this version, but it has been tested and proven to work on Python 2.6 and
greater, thanks to some hacky module scripting.

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
This may not hold true for other Operating Systems.

If the load time is consistently slow across major platforms, and no
reasonable solutions emerge, then it may not be worth making the
transition.

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
