#!/usr/bin/env python

import os.path
import json

CONFIG_FILE = "config"
class Logger:

	def __init__(self):
		if not os.path.isfile(CONFIG_FILE):
			print "generating config file"
			f = open(CONFIG_FILE, "w+")
		else:
			f = open(CONFIG_FILE, "r")

		self.channels = {}
		# init msg queues here
		# queue is a dict of msg ids

		try:
			self.channels = json.load(f, parse_int=int())
		except ValueError:
			print "Can't parse config!"

		f.close()
		#print self.channels

	def updateLog(self, server, logchannel):
		server = str(server)
		logchannel = int(logchannel)
		if not self.channels.has_key(server):
			self.channels[server] = [0]
		self.channels[server][0] = logchannel
		# rewrite channels file
		self.writeConfig()

	def ignoreChannel(self, server, channel):
		server = str(server)
		channel = int(channel)
		try:
			index = self.channels[server][1:].index(channel)
			del self.channels[server][index + 1]
			self.writeConfig()
			return False
		except ValueError:
			self.channels[server].append(channel)
			self.writeConfig()
			return True

	def writeConfig(self):
		with open(CONFIG_FILE, "w") as config_file:
			json.dump(self.channels, config_file)
			#for key,value in self.channels.items():
			#	line = "{},{}\n".format(key,value)
			#	config_file.write(line)

	def getLogChannel(self, server):
		server = str(server)
		if self.channels.has_key(server):
			return self.channels[server][0]
		else:
			return None

if __name__ == "__main__":
	l = Logger()
	l.updateLog(10,20)
	l.ignoreChannel(10,30)
	#l.writeConfig()
