from system.base_plugin import BasePlugin

import re

class Plugin(BasePlugin):

	name     = 'ip_filter'
	name     = 'IP Chat Filter'
	version  = '1.0'

	def on_player_chat(self, player, message):
		return re.sub(r'[0-9]+(?:\.[0-9]+){3}', "^1[do not advertise]^7", message)