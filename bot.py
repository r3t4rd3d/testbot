#!/usr/bin/env python3
from disco.bot import Bot, Plugin
import datetime

class SimplePlugin(Plugin):
	#@Plugin.listen('ChannelCreate')
	#def on_channel_create(self, event):
	#	event.channel.send_message('Nice channel m8!')

	# default message listener
	@Plugin.listen('MessageCreate')
	def message_send(self, msg):
		timestamp = msg.timestamp.fget().strftime('%Y-%m-%dT%H:%M:%S')
		output = "[" + timestamp + "]," + msg.author.username + " :" + msg.content
		print output

	# message update listener
	@Plugin.listen('MessageUpdate')
	def message_update(self, msg):
		timestamp = msg.edited_timestamp.fget().strftime('%Y-%m-%dT%H:%M:%S')
		output = "[" + timestamp + "]E," + msg.author.username + " :" + msg.content
		print output

	@Plugin.command('ping')
	def on_ping_command(self, event):
		event.msg.reply('Stop pinging me!')

	@Plugin.command('info', '<query:str...>')
	def on_info(self, event, query):
		users = list(self.state.users.select({'username': query}, {'id': query}))

		if not users:
			event.msg.reply("Couldn't find user for your query: `{}`".format(query))
		elif len(users) > 1:
			event.msg.reply('I found too many userse ({}) for your query: `{}`'.format(len(users), query))
		else:
			user = users[0]
			parts = []
			parts.append('ID: {}'.format(user.id))
			parts.append('Username: {}'.format(user.username))
			parts.append('Discriminator: {}'.format(user.discriminator))

			if event.channel.guild:
				member = event.channel.guild.get_member(user)
				parts.append('Nickname: {}'.format(member.nick))
				parts.append('Joined At: {}'.format(member.joined_at))

			event.msg.reply('```\n{}\n```'.format('\n'.join(parts)))
