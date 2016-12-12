#!/usr/bin/env python

import os.path

CONFIG_FILE = "config"
class Logger:

	def __init__(self):
		if not os.path.isfile(CONFIG_FILE):
			print "generating config file"
			f = open(CONFIG_FILE, "w+")
		else:
			f = open(CONFIG_FILE, "r")

		self.channels = {}
		lines = f.read().splitlines();
		for line in lines:
			channel = line.split(",")
			if len(channel) == 2:
				self.channels[int(channel[0])] = int(channel[1])

		f.close()
		#print self.channels

	def update(self, server, channel):
		if channel != 0:
			self.channels[server] = channel
		else:
			if self.channels.has_key(server):
				del self.channels[server]
		# rewrite channels file
		self.writeDict()

	def writeDict(self):
		with open(CONFIG_FILE, "w") as config_file:
			for key,value in self.channels.items():
				line = "{},{}\n".format(key,value)
				config_file.write(line)

	def getChannel(self, server):
		if self.channels.has_key(server):
			return self.channels[server]
		else:
			return None

if __name__ == "__main__":
	l = Logger()
