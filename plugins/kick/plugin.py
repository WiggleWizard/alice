from system.base_plugin import BasePlugin

from system.player import Player
from string import Template

class Plugin(BasePlugin):
	
	name         = 'kick'
	display_name = 'kick'
	requires     = ['advanced_commands']

	def on_plugin_init(self):
		
		# Register command
		command_plugin = self.get_plugin("advanced_commands")
		command_plugin.register_command(self.command_kick, 'kick', 2);

	def command_kick(self, executor, args): 

		identifier = args.pop(0)
		reason = ' '.join(args);

		print "ident "+identifier
		print "reason "+reason

		try:
			if(len(args) > 2):
				raise ValueError

			pid = int(args[0])
			if(pid >= self._alice.get_max_players()):
				raise ValueError

			self._alice._players[pid].kick(reason);

		except ValueError: # not an id
			# find the players name
			players = self._alice.find_player_by_partialEx(identifier);
			if(len(players) == 0):
				executor.tell('^1no matching player')
				return

			if(len(players) > 1):
				executor.tell('^1more than one matching players ('+', '.join(['['+str(p.get_id())+'] '+str(p.get_clean_name()) for p in players])+')')
				return

			players[0].kick(reason);
