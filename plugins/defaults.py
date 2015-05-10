from system.base_plugin import BasePlugin

class Plugin(BasePlugin):
	
	name    = 'Defaults Plugin'
	version = '1.0'

	def on_plugin_init(self):
		command_plugin = self.get_plugin("adv_commands")

		command_plugin.register_command(self.command_pizza, "pizza", 0)

	def on_join_req(self, ip, qport):
		self.accept_ip(ip, qport)

	def on_player_chat(self, player, message):
		#self.broadcast_chat(str(player) + ": " + message)
		pass

	def command_pizza(self, executor, args):
		self.broadcast_chat(executor.get_clean_name() + " has started eating a pizza")