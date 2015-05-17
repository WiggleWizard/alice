from system.base_plugin import BasePlugin

from system.player import Player
from string import Template

class Plugin(BasePlugin):
	
	name         = 'kick'
	display_name = 'kick'
	requires     = ['advanced_commands']

	def on_plugin_init(self):
		
		# Register command
		self._cmd_pid = Command("kick", self.command_pid, None, "!kick <pid> <reason>");
		self._cmd_pid.add_argument("pid", int, "Player ID", 1);
		self._cmd_pid.add_argument("reason", str, "reason for kick", "+");
		
		self._cmd_name = Command("kick", self.command_pname, None, "!kick <pname> <reason>");
		self._cmd_name.add_argument("pname", str, "Player Name", 1);
		self._cmd_name.add_argument("reason", str, "reason for kick", "+");

		command_plugin = self.get_plugin("advanced_commands")
		command_plugin.register_command(self._cmd_pid);
		command_plugin.register_command(self._cmd_name);

	def command_pid(self, executor, args): 

		if(args.pid[0] >= self._alice.get_max_players()):
			executor.tell('^1invalid player id')
			return

		player = self._alice._players[args.pid[0]];
		if player != None:
			player.kick(' '.join(args.reason))
		else:
			executor.tell('^1player with id '+str(args.pid[0])+' does not exist')

	def command_pname(self, executor, args): 
		players = self._alice.find_player_by_partialEx(args.pname[0]);
		if(len(players) == 0):
			executor.tell('^1no matching player')
			return

		if(len(players) > 1):
			executor.tell('^1more than one matching players ('+', '.join(['['+str(p.get_id())+'] '+str(p.get_clean_name()) for p in players])+')')
			return

		players[0].kick(' '.join(args.reason));



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
