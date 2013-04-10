EpiPlanning
===========

A little python 2.x script to get the next appointments from new Epitech Intra

## Features

Without arguments, the script ask you for your credentials first then print your next appointments.

	$ ./planning.py
	Activity  0
	Name :  Présentation de la nouvelle Direction Générale
	Type :  event
	Starting :  2013-04-10 18:00:00
	Ending :  2013-04-10 19:00:00
	Starting in :  8h46
	Room :  Amphi

	Activity  1
	Name :  STEPHANIE 8
	Type :  event
	Starting :  2013-04-11 12:00:00
	Ending :  2013-04-11 14:00:00
	Starting in :  2h46
	Room :  Susie-dimension

The -n option only print the next appintment on one line.

	$ ./planning.py -n
	Présentation de - Amphi -> 8h41

The -p option allow you to purge the cache (3 hours by default).

## Installation

First, clone the repository in a folder of your choice :

	$ git clone https://github.com/geekuillaume/EpiPlanning.git

You only need one python lib to use it, [requests](http://docs.python-requests.org/en/latest/).
To install it, use [pip](http://www.pip-installer.org/en/latest/):

	$ pip install requests

## TODO

* Add a daemon mode to display notifications before appoitments
* Export all in the iCal format
* You tell me !

## Credits

Script created by [Guillaume Besson](http://besson.co/) ([geekuillaume](http://geekuillau.me/))