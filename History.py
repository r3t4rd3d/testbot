#!/usr/bin/env python

from collections import deque
MAX_DEPTH = 100 #max number of messages per channel
class History:
	def __init__(self, channel):
		# create message dict and message age list
		self.messages = {}
		self.age = deque()

		message_iterator = channel.messages_iter(bulk=True, chunk_size = MAX_DEPTH)
		try:
			messages = message_iterator.next()
			for message in messages:
				self.addMessage(message)
		except StopIteration:
			pass
		
	def addMessage(self, message):
		self.messages[message.id] = message
		self.age.append(message.id)
		if len(self.age) > MAX_DEPTH:
			oldID = self.age.popleft()
			del self.messages[oldID]

	def updateMessage(self, message):
		if message.id in self.messages:
			self.messages[message.id] = message

	def dereference(self, index):
		return self.messages[self.age[index]]
	
	def getMessage(self, messageid):
		return self.messages[messageid]
