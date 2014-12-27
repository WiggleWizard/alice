from plugins.adv_commands_data.base_command import BaseCommand

class Command(BaseCommand):
	def __init__(self):
		self.alias       = "perm"
		self.description = "Prints the details of either the target player or the current player"
		self.args        = 0

	def execute(self, executor, args):
		# Detail self, allowed with no permissions
		if len(args) == 0:
			self._tell_details(executor, executor)
		else:
			print(self.find_players_by_partial(args[0]))


	def _tell_details(self, to_player, of_player):
		to_player.tell("IP: " + of_player.get_ip())