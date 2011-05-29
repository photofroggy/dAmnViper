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
    
    from dAmnViper.base import ReconnectingClient
    
    dAmn = ReconnectingClient()
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

I know it is a bad idea to not use Twisted, but this library was
intended for use in applications where the target audience is not likely
to want to spend time installing program after program. The idea was to
allow the user to get the application working as quickly as possible.

I will be experimenting with Twisted in the near future and may
re-release dAmn Viper using Twisted for managing the connection.

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
