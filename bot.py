#!/usr/bin/env python3
from disco.bot import Bot, Plugin
from disco.types.permissions import PermissionValue, Permissions, Permissible
from disco.types.user import Game, GameType, Status
from disco.types.message import MessageEmbed
import datetime
import random
from Logger import Logger
from History import History

R3TID = 165778877354868737
taunts = ['is a faggot', 'is the coolest person on the planet', 'isn\'t worth my CPU time']
s_names = ['dank memes', 'NSA', 'generating memes', 'always watching', 'nothing', 'GVIM', '421-1', '910+1']

class KekbotPlugin(Plugin):
	def load(self, ctx):
		super(KekbotPlugin, self).load(ctx)
		#print self.state.guilds
		self.logger = Logger()

	def unload(self, ctx):
		super(KekbotPlugin, self).unload(ctx)

	@Plugin.listen('Ready')
	def ready(self, event):
		game = Game(type=GameType.DEFAULT, name=random.choice(s_names))
		self.client.update_presence(game=game, status=Status.ONLINE)

	@Plugin.schedule(interval=30, init=False)
	def update_status(self):
		game = Game(type=GameType.DEFAULT, name=random.choice(s_names))
		self.client.update_presence(game=game, status=Status.ONLINE)

	@Plugin.listen('GuildCreate')
	def guild_init(self, event):
		guild = event.guild
		self.logger.addGuild(guild)
		print 'Finished building message history for guild:{}'.format(event.guild.id)

	# default message listener
	@Plugin.listen('MessageCreate')
	def message_send(self, msg):
		if msg.channel.is_dm:
			print "{}: {}".format(msg.author.username, msg.content)
			return

		# ignore bot messages
		if bool(msg.author.id):
			# ingore dms
			try:
				self.logger.addMessage(msg)
			except AttributeError:
				pass
		#perms = msg.guild.get_permissions(msg.author).to_dict()
		#timestamp = msg.timestamp.fget().strftime('%Y-%m-%dT%H:%M:%S')

	@Plugin.listen('MessageUpdate')
	def message_updated(self, msg):
		# ignore bot messages
		if not bool(msg.author.id):
			return
		if msg.guild is not None:
			try:
				logchannel = self.logger[msg.guild.id]
				msg_old = self.logger.getHistory(msg.guild.id, msg.channel.id).getContent(msg.id)
				self.logger.updateMessage(msg)

				embed = MessageEmbed()
				embed.title = 'Message updated in: **#{}**'.format(msg.channel.name)
				embed.description = '**{}**\n***old:***\n{}\n***new:***\n{}'.format(msg.author.username.encode("ascii","ignore"), msg_old, msg.content)
				embed.color = int("1388D6", 16)
				#embed.set_author(name = '{}:'.format(msg.author.username))
				#embed.add_field(name = 'old:', value = msg_old)
				#embed.add_field(name = 'new:', value = msg.content)

				msg.guild.channels[logchannel].send_message('', embed = embed)
			except KeyError:
				pass

	@Plugin.listen('MessageDelete')
	def message_delete(self, event):
		channel = self.state.channels[event.channel_id]
		server = channel.guild
		# ignore bot messages
		#if not bool(msg.author.id):
		#	return
		if server is not None:
			logchannel = self.logger[server.id]
			try:
				message = self.logger.getHistory(server.id, channel.id)[event.id]
				# ingore embed only messages
				if not bool(message.content):
					return

				embed = MessageEmbed()
				embed.title = "Message deleted in: **#{}**".format(channel.name)
				embed.description = '**{}**\n{}'.format(message.author.username.encode("ascii","ignore"), message.content)
				embed.color = int("D3262E", 16)
				#embed.type = 'fields'
				#embed.add_field(name = message.author.username, value = message.content)
				server.channels[logchannel].send_message('', embed = embed)

			except KeyError:
				pass

	@Plugin.command('github')
	def on_cmd_github(self, event):
		event.msg.reply('https://github.com/r3t4rd3d/testbot')

	@Plugin.command('verify')
	def on_cmd_verify(self, event):
		if event.msg.author.id == R3TID:
			event.msg.reply('Hello Creator!')

	@Plugin.command('test')
	def on_test(self, event):
		if event.msg.author.id == R3TID:
			msg = event.msg
			embed = MessageEmbed()
			embed.title = 'Message updated in: #{}'.format(msg.channel.name)
			embed.description = '**{}**'.format(msg.author.username)
			embed.color = int("1388D6", 16)

			msg.reply('', embed=embed)

	@Plugin.command('help')
	def on_help(self, event):
		embed = MessageEmbed()
		embed.type = 'fields'
		embed.title = 'HELP'
		embed.add_field(name='!taunt [@user]', value='Taunt user')
		embed.add_field(name='!log <int>', value='Send log messages to the current channel if int > 0, logging is disabled if this condition is not true. [Requires admin permissions]')
		embed.add_field(name='!logignore', value='Ignore/Log channel. [Requires admin permissions]')

		event.msg.reply('', embed=embed)

	@Plugin.command('taunt')
	def on_taunt(self, event):
		msg = event.msg
		target = msg.author
		mentions = msg.mentions.values()
		try:
			target = next(mentions)
		except StopIteration:
			pass

		msg.reply('{} {}!'.format(target.mention, random.choice(taunts)))

	@Plugin.command('log', '<switch:int>')
	def on_log(self, event, switch):
		try:
			perms = event.msg.guild.get_permissions(event.msg.author)
			#print perms.can(Permissions.ADMINISTRATOR)
			if not perms.can(Permissions.ADMINISTRATOR):
				event.msg.reply("<@{}> This command requires admin permissions!".format(event.msg.author.id))
				return

			serverid = event.msg.guild.id
			channelid = event.msg.channel_id
			if switch > 0:
				event.msg.reply("Logging to this channel")
				self.logger.updateLog(serverid, channelid)
			else:
				event.msg.reply("Server logging disabled")
				self.logger.updateLog(serverid, 0)
		except AttributeError:
			 event.msg.reply("This command can't be used in dms!")

	@Plugin.command('logignore')
	def logignore(self, event):
		try:
			perms = event.msg.guild.get_permissions(event.msg.author)
			if not perms.can(Permissions.ADMINISTRATOR):
				event.msg.reply("<@{}> This command requires admin permissions!".format(event.msg.author.id))
				return

			guild_id = event.msg.guild.id
			channel_id = event.msg.channel_id
			ignore = self.logger.ignoreChannel(guild_id, channel_id)
			if ignore:
				event.msg.reply('Ignoring this channel')
			else:
				event.msg.reply('Logging channel messages')

		except (AttributeError, KeyError):
			pass

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
