#!/usr/bin/env python

from collections import deque
import copy

MAX_DEPTH = 100 #max number of messages per channel
class History:
	def __init__(self, channel):
		# create message dict and message age list
		self.messages = {}
		self.content = {}
		self.age = deque()

		messages = channel.messages_iter(bulk=True, chunk_size = MAX_DEPTH).next()
		for m in messages:
			self.addMessage(m)

	def addMessage(self, message):
		self.messages[message.id] = message
		self.content[message.id] = copy.copy(message.content)
		self.age.append(message.id)
		if len(self.age) > MAX_DEPTH:
			oldID = self.age.popleft()
			del self.messages[oldID]
			del self.content[oldID]

	def updateMessage(self, message):
		if message.id in self.messages:
			self.messages[message.id] = message
			self.content[message.id] = copy.copy(message.content)

	def dereference(self, index):
		return self.messages[self.age[index]]
	
	def getMessage(self, messageid):
		return self.messages[messageid]

	def __getitem__(self, key):
		return self.messages[key]

	def getContent(self, messageid):
		return self.content[messageid]
