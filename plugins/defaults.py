from system.base_plugin import BasePlugin

class Plugin(BasePlugin):
	
	name    = 'Defaults Plugin'
	version = '1.0'

	def on_plugin_init(self):
		pass

	def on_join_req(self, ip, qport):
		self.accept_ip(ip, qport)

	def on_player_chat(self, player, message):
		self.broadcast_chat(str(player) + ": " + message)