#!/usr/bin/env python3
from disco.bot import Bot, Plugin
from disco.types.permissions import PermissionValue, Permissions, Permissible
import disco.types.message
import datetime
from Logger import Logger
from History import History

autorID = 165778877354868737
def verify(msg):
	content = msg.content
	mentions = list(msg.mentions.values())

	if content == "!verify" and msg.author.id == autorID:
		msg.reply('Hello creator!')

	elif content == "!github":
		msg.reply('https://github.com/r3t4rd3d/testbot')

	elif content == "!test":
		embed = disco.types.message.MessageEmbed()
		embed.title = 'Test!'
		embed.description = 'extensive testing'
		embed.color = int("D3262E", 16)
		print embed.to_dict()
		msg.reply('', embed=embed)
		#test history object
		#htest = History(msg.channel)


	elif content.startswith("!taunt"):
		target = msg.author.id
		if len(mentions) > 0:
			target = mentions[0].id

		msg.reply('<@{}> is a faggot!'.format(target))

class SimplePlugin(Plugin):
	def __init__(self, bot, config):
		super(SimplePlugin, self).__init__(bot, config)
		self.logger = Logger()


	# default message listener
	@Plugin.listen('MessageCreate')
	def message_send(self, msg):
		verify(msg)
		if msg.channel.is_dm:
			print "{}: {}".format(msg.author.username, msg.content)
		#perms = msg.guild.get_permissions(msg.author).to_dict()
		#for key,value in perms.items():
		#	print "{}:{}".format(key,value)
		#timestamp = msg.timestamp.fget().strftime('%Y-%m-%dT%H:%M:%S')
		#output = "[" + timestamp + "]," + msg.author.username + ":" + msg.content
		#print output

	@Plugin.listen('MessageUpdate')
	def message_updated(self, msg):
		#print bool(msg.author.id)
		if bool(msg.author.id):
			output = "<@{}> edited message in <#{}>: {}".format(msg.author.id, msg.channel_id, msg.content)
			#print output
			if msg.guild is not None:
				logchannel = self.logger.getLogChannel(msg.guild.id)
				if logchannel is not None:
					msg.guild.channels[logchannel].send_message(output)

	@Plugin.listen('MessageDelete')
	def message_delete(self, event):
		#print event.id
		output = "Message deleted in: <#{}>".format(event.channel_id)
		#print output
		server = self.state.channels[event.channel_id].guild

		if server is not None:
			logchannel = self.logger.getLogChannel(server.id)
			if logchannel is not None and logchannel !=0:
				server.channels[logchannel].send_message(output)

	@Plugin.command('ping')
	def on_ping_command(self, event):
		event.msg.reply('Stop pinging me!')

	@Plugin.command('log', '<switch:int>')
	def on_log(self, event, switch):
		try:
			perms = event.msg.guild.get_permissions(event.msg.author)
			#print perms.can(Permissions.ADMINISTRATOR)
			if perms.can(Permissions.ADMINISTRATOR):
				serverid = event.msg.guild.id
				channelid = event.msg.channel_id
				if switch > 0:
					event.msg.reply("Logging to this channel")
					self.logger.updateLog(serverid, channelid)
				else:
					event.msg.reply("Server logging disabled")
					self.logger.updateLog(serverid, 0)
			else:
				event.msg.reply("<@{}> This command requires admin permissions!".format(event.msg.author.id))
		except AttributeError:
			 event.msg.reply("This command can't be used in dms!")

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
