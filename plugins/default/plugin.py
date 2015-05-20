from system.base_plugin import BasePlugin

class Plugin(BasePlugin):
	
	name         = 'default'
	display_name = 'Default Plugin'
	version      = '1.0'

	def on_plugin_init(self):
		pass

	def on_join_req(self, slot_id, player_ip, player_guid, player_name):
		self.limbo_deny(slot_id, "TEST")

	def on_player_chat(self, player, message):
		message = str(player) + ": " + message;
		self.broadcast_chat(message)
		return message
