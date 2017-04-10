#!/usr/bin/env python

import os.path
import json
from collections import defaultdict
from History import History

CONFIG_FILE = "config"
class Logger:

	def __init__(self):
		if not os.path.isfile(CONFIG_FILE):
			print "generating config file"
			f = open(CONFIG_FILE, "w+")
		else:
			f = open(CONFIG_FILE, "r")

		self.channels = defaultdict(list)
		# init msg queues here
		# queue is a dict of msg ids
		self.histories = defaultdict(dict)

		try:
			self.channels = json.load(f, parse_int=int())
		except ValueError:
			print "Can't parse config!"

		f.close()
		#print self.channels

	def updateLog(self, server, logchannel):
		server = str(server)
		logchannel = int(logchannel)
		#if not self.channels.has_key(server):
		#	self.channels[server] = [0]
		self.channels[server][0] = logchannel
		# rewrite channels file
		self.writeConfig()

	def ignoreChannel(self, server, channel):
		server = str(server)
		channel = int(channel)
		try:
			# check if channel is already on the ignore list
			index = self.channels[server][1:].index(channel)
			del self.channels[server][index + 1]
			self.writeConfig()
			return False
		except ValueError:
			# add channel to the ignore list
			self.channels[server].append(channel)
			self.writeConfig()
			return True

	def writeConfig(self):
		with open(CONFIG_FILE, "w") as config_file:
			json.dump(self.channels, config_file)

	def getLogChannel(self, server):
		server = str(server)
		return self.channels[server][0]

	def addGuild(self, guild):
		#self.histories[guild.id] = {}
		ch_histories = self.histories[guild.id]
		for channel in guild.channels.itervalues():
			try:
				ch_histories[channel.id] = History(channel)
			except:
				pass

	def addMessage(self, msg):
		channel_id = msg.channel_id
		guild_id = msg.guild.id
		try:
			self.histories[guild_id][channel_id].addMessage(msg)
		except KeyError:
			pass
	
	def getHistory(self, guild_id, channel_id):
		if channel_id not in self.channels[str(guild_id)][1:]:
			return self.histories[guild_id][channel_id]
		else:
			raise KeyError()

	def updateMessage(self, msg):
		channel_id = msg.channel_id
		guild_id = msg.guild.id
		self.getHistory(guild_id, channel_id).updateMessage(msg)

if __name__ == "__main__":
	l = Logger()
	l.updateLog(10,20)
	l.ignoreChannel(10,30)
	#l.writeConfig()
