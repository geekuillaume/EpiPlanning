#! /usr/bin/python

import requests
import getpass
import json
from datetime import datetime
import time
import ConfigParser
import argparse
import os

def main():
	parser = argparse.ArgumentParser(description='Getting next appointments from new Epitech Intra')
	parser.add_argument('-n', dest="onlyNext", const=True, default=False, action='store_const', help="Only print next appointment")
	parser.add_argument('-p', dest="purge", const=True, default=False, action='store_const', help="Purge all cached values")
	args = parser.parse_args()
	auth = getCookie(args.purge)
	getPlanning(auth, args.onlyNext, args.purge)
	return

def daemonRun():
	while True:

		sleep(5)

def execDaemon(action):
	pid = os.path.dirname(os.path.abspath(__file__)) + '/daemon.pid'
	daemon = Daemonize(app="EpiPlanning", pid=pid, action=daemonRun)
	daemon.start()

def writeConfig(login, password, cookie):
	config = ConfigParser.RawConfigParser()
	config.add_section('user')
	config.set('user', 'login', login)
	config.set('user', 'password', password)
	config.set('user', 'cookie', cookie)
	with open(os.path.dirname(os.path.abspath(__file__)) + '/config.cfg', 'wb') as configfile:
		config.write(configfile)

def getUser():
	config = ConfigParser.RawConfigParser()
	try:
		config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.cfg')
		login = config.get('user', 'login')
		password = config.get('user', 'password')
		cookie = config.get('user', 'cookie')
	except:
		login = raw_input("Login: ")
		password = getpass.getpass("Password: ")
		cookie = False
	return login, password, cookie

def getCookie(force):
	login, password, cookie = getUser()

	if not force and cookie:
		return cookie

	url = 'https://intra.epitech.eu/'
	values = {	'login': login,
				'password': password,
				'remind': 'on' }

	r = requests.post(url, data=values)
	if r.status_code is not 200:
		print("Mauvais Login ou MDP");
		exit(1);
	writeConfig(login, password, r.cookies['auth'])
	return r.cookies['auth']

def getPlanning(cookie, onlyNext, force):
	url = 'https://intra.epitech.eu/user/notification/coming?format=json'
	cookies = dict(auth=cookie)
	cache = dict()

	config = ConfigParser.RawConfigParser()
	try:
		config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.cfg')
		cache["content"] = config.get('cache', 'content')
		cache["timestamp"] = config.getint('cache', 'timestamp')
		if time.time() - cache["timestamp"] > 60*60*3:
			force = True
	except:
		force = True

	if force:
		r = requests.get(url, cookies=cookies)

		if r.status_code is not 200:
			cookie = getCookie(True)
			cookies = dict(auth=cookie)
			r = requests.get(url, cookies=cookies)

		cache["content"] = r.content[31:]
		cache["timestamp"] = int(time.time())
		if not config.has_section('cache'):
			config.add_section('cache')
		config.set('cache', 'content', cache["content"])
		config.set('cache', 'timestamp', cache["timestamp"])
		with open(os.path.dirname(os.path.abspath(__file__)) + '/config.cfg', 'wb') as configfile:
			config.write(configfile)


	activities = json.loads(cache["content"])

	if onlyNext:
		if len(activities) == 0:
			print "Nothing to do"
			exit(0)
		if activities[0]["room"]:
			print activities[0]["title"][:15], "-", activities[0]["room"].rsplit('/', 1)[1], "->", strRelativeDate(datetime.strptime(activities[0]["begin"], "%Y-%m-%d %H:%M:%S"))
		else:
			print activities[0]["title"][:15], "->", strRelativeDate(datetime.strptime(activities[0]["begin"], "%Y-%m-%d %H:%M:%S"))
		exit(0)

	for i, activity in enumerate(activities):
		print "\nActivity ", i
		print "Name : ", activity["title"]
		print "Type : ", activity["status"]
		print "Starting : ", datetime.strptime(activity["begin"], "%Y-%m-%d %H:%M:%S")
		print "Ending : ", datetime.strptime(activity["end"], "%Y-%m-%d %H:%M:%S")
		print "Starting in : ", strRelativeDate(datetime.strptime(activity["begin"], "%Y-%m-%d %H:%M:%S"))
		if activity["room"]:
			print "Room : ", activity["room"].rsplit('/', 1)[1]

	return

def strRelativeDate(dateTo):
	str = ""
	duree = dateTo - datetime.now()
	if duree.days > 1:
		str += "%d days, "%(duree.days,)
	str += "%dh%d"%(duree.seconds / 3600, (duree.seconds / 60) % 60,)
	return str

main()
