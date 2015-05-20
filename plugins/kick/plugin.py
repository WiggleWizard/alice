from system.base_plugin import BasePlugin

from system.player import Player
from string import Template

class Plugin(BasePlugin):
	
	name         = 'kick'
	display_name = 'Kick'
	requires     = ['advanced_commands']

	def on_plugin_init(self):
		command_plugin = self.get_plugin("advanced_commands")

		cmd = command_plugin.register_command(["k", "kick"], self.command_kick, None)
		cmd.add_param(
			"players",
			command_plugin.filter_player_search,
			"id/player name",
			"Slot ID or a partial name"
		)

	def command_kick(self, executor, args, free_text):
		print(args)
