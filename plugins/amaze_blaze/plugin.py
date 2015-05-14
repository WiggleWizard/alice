from system.base_plugin import BasePlugin

from system.player import Player

class Plugin(BasePlugin):
	
	name         = 'amaze_blaze'
	display_name = 'Amaze Blaze'
	version      = '420.0'
	requires     = ['advanced_commands']

	def on_plugin_init(self):
		# Extend player
		Player.is_blazing = False

		# Register command
		command_plugin = self.get_plugin("advanced_commands")
		command_plugin.register_command(self.command_420, "420", 0)

	def on_player_dc(self, player):
		player.is_blazing = False

	def command_420(self, executor, args):
		# Wants to pass his blaze on to another player
		if len(args) > 0:
			if not executor.is_blazing:
				executor.tell("You must be blazing before you can hand out your amaze blaze")
			else:
				player_search = self.find_players_by_partial(args[0])

				if len(player_search) > 0:
					# Found a specific player to blaze with
					if len(player_search) == 1:
						self.broadcast_chat(executor.get_clean_name() + " passed his amaze blaze to " + player_search[0].get_clean_name())
						executor.is_blazing = False
					else:
						executor.tell("Multiple players found, please be more specific if you want to blaze it")
				else:
					executor.tell("Could not find any player to blaze with, forever alone?")
		# Player lights his own blaze
		else:
			executor.is_blazing = True
			self.broadcast_chat(executor.get_clean_name() + " has started blazing it")