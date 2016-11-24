#!/usr/bin/env python3
from disco.bot import Bot, Plugin

class SimplePlugin(Plugin):
	@Plugin.listen('ChannelCreate')
	def on_channel_create(self, event):
		event.channel.send_message('Nice channel m8!')

	@Plugin.command('ping')
	def on_ping_command(self, event):
		event.msg.reply('Stop pinging me!')
