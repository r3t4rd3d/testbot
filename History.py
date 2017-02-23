#!/usr/bin/env python

from collections import deque
MAX_DEPTH = 100 #max number of messages per channel
class History:
	def __init__(self, channel):
		# create message dict and message age list
		self.messages = {}
		self.age = deque()

		message_iterator = channel.messages_iter(chunk_size = MAX_DEPTH)
		for i in range(1, MAX_DEPTH):
			try:
				message = message_iterator.next()
				self.addMessage(message)
			except StopIteration:
				break
		
	def addMessage(self, message):
		self.messages[message.id] = message
		self.age.append(message.id)
		if len(self.age) > MAX_DEPTH:
			oldID = self.age.popleft()
			del self.messages[oldID]

	def dereference(self, index):
		return self.messages[self.age[index]]
	
	def getMessage(self, messageid):
		return self.messages[messageid]
