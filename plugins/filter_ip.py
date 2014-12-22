from system.base_plugin import BasePlugin

import re

class Plugin(BasePlugin):
	def __init__(self):
		super(BasePlugin, self).__init__()
		
		self.name     = 'IP Chat Ad Filter'
		self.version  = '1.0'

	def on_player_chat(self, player, message):
		filtered = re.sub(r'[0-9]+(?:\.[0-9]+){3}', "^1[do not advertise]^7", message)

		return filtered