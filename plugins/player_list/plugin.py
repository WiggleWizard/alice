from system.base_plugin import BasePlugin

from system.player import Player
from string import Template

class Plugin(BasePlugin):
	
	name         = 'player_list'
	display_name = 'Player List'
	requires     = ['advanced_commands']

	def on_plugin_init(self):
		# Config registers
		self._fmt_entry = self.config.get('entry_format', "[${id}] ${clean_name}^7")
		self._entries_per_page = self.config.get('entries_per_page', 6)
		self._logged_in_color = self.config.get('logged_in_color', "^2")
		self._logged_out_color = self.config.get('logged_out_color', "^4")

		# Register command
		self._cmd_list = Command("p", self.command_p, None, "!p <pageid>(optional)");
		self._cmd_list.add_argument("pageid", int, "page id", "?");

		command_plugin = self.get_plugin("advanced_commands")
		command_plugin.register_command(self._cmd_list);


	# list all players
	def command_p(self, executor, args): 

		if(args.pageid == None):
			for player in self._alice._players: # print all, no parameter
				if player != None:
					executor.tell(self._format_entry(player))
			return

		if(args.pageid < 0):
			executor.tell('^1Parameter needs to be a number >=0')
			return

		i = 0
		for player in self._alice._players: # print a page of 5 players
			if player != None:
				if i >= args.pageid * self._entries_per_page and i < (args.pageid+1) * self._entries_per_page:
					executor.tell(self._format_entry(player))
				i+=1


	##
	# Decorates with the player's information.
	##
	def _format_entry(self, player):
		d = dict(
			id         = player.get_id(),
			clean_name = player.get_clean_name(),
			ip         = player.get_ip()
		)

		return Template(self._fmt_entry).safe_substitute(d)