#!/usr/bin/env python3
from disco.bot import Bot, Plugin
from disco.types.permissions import PermissionValue, Permissions, Permissible
from disco.types.user import Game, GameType, Status
import disco.types.message
import datetime
import random
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
		#embed = disco.types.message.MessageEmbed()
		#embed.title = 'Test!'
		#embed.description = 'extensive testing'
		#embed.color = int("D3262E", 16)
		#print embed.to_dict()
		htest = History(msg.channel)
		text = '```{}```'.format(htest.dereference(0).to_dict())
		msg.reply(text)
		#test history object


	elif content.startswith("!taunt"):
		target = msg.author.id
		if len(mentions) > 0:
			target = mentions[0].id

		msg.reply('<@{}> is a faggot!'.format(target))

s_names = ['dank memes', 'NSA', 'generating memes', 'always watching', 'nothing', 'GVIM', '421-1', '910+1']
game = Game()
game.type = GameType.DEFAULT

class SimplePlugin(Plugin):
	def __init__(self, bot, config):
		super(SimplePlugin, self).__init__(bot, config)
		#print self.state.guilds
		self.logger = Logger()

	@Plugin.listen('Ready')
	def ready(self, event):
		game.name = random.choice(s_names)
		self.client.update_presence(game=game, status=Status.ONLINE)

	@Plugin.schedule(interval=30, init=False)
	def update_status(self):
		game.name = random.choice(s_names)
		self.client.update_presence(game=game, status=Status.ONLINE)

	@Plugin.listen('GuildCreate')
	def guild_init(self, event):
		#print event.guild.channels
		guild = event.guild
		print 'Building message history for guild:{}'.format(event.guild.id)
		self.logger.addGuild(guild)
		print 'Done!'
		#try:
		#	print self.logger.histories[guild.id][230144298191028225].dereference(0).to_dict()
		#except KeyError:
		#	print "Key Error!"

	# default message listener
	@Plugin.listen('MessageCreate')
	def message_send(self, msg):
		verify(msg)
		if msg.channel.is_dm:
			print "{}: {}".format(msg.author.username, msg.content)

		# ignore bot messages
		if bool(msg.author.id):
			# ingore dms
			try:
				self.logger.addMessage(msg)
			except AttributeError:
				pass
		#perms = msg.guild.get_permissions(msg.author).to_dict()
		#for key,value in perms.items():
		#	print "{}:{}".format(key,value)
		#timestamp = msg.timestamp.fget().strftime('%Y-%m-%dT%H:%M:%S')
		#output = "[" + timestamp + "]," + msg.author.username + ":" + msg.content
		#print output

	@Plugin.listen('MessageUpdate')
	def message_updated(self, msg):
		#output = "<@{}> edited message in <#{}>: {}".format(msg.author.id, msg.channel_id, msg.content)
		#print msg.to_dict()
		# ignore bot message
		if not bool(msg.author.id):
			return
		if msg.guild is not None:
			try:
				logchannel = self.logger.getLogChannel(msg.guild.id)
				msg_old = self.logger.histories[msg.guild.id][msg.channel.id].getContent(msg.id)
				self.logger.updateMessage(msg)
				embed = disco.types.message.MessageEmbed()
				embed.title = 'Message updated in: #{}'.format(msg.channel.name)
				embed.color = int("1388D6", 16)
				embed.type = 'fields'
				embed.set_author(name = '{}:'.format(msg.author.username))
				embed.add_field(name = 'old:', value = msg_old)
				embed.add_field(name = 'new:', value = msg.content)

				msg.guild.channels[logchannel].send_message('', embed = embed)
			except KeyError:
				pass

	@Plugin.listen('MessageDelete')
	def message_delete(self, event):
		#print event.id
		channel = self.state.channels[event.channel_id]
		server = channel.guild

		# ignore bot messages
		#if not bool(msg.author.id):
		#	return
		if server is not None:
			logchannel = self.logger.getLogChannel(server.id)
			try:
				output = "Message deleted in: #{}".format(channel.name)
				embed = disco.types.message.MessageEmbed()
				embed.title = output
				embed.color = int("D3262E", 16)
				embed.type = 'fields'
				message = self.logger.histories[server.id][channel.id].getMessage(event.id)

				# ingore embed only messages
				if not bool(message.content):
					return

				embed.add_field(name = message.author.username, value = message.content)
				server.channels[logchannel].send_message('', embed = embed)
			except KeyError:
				pass

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
