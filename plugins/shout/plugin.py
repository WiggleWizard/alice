from system.base_plugin import BasePlugin

from system.player import Player
from string import Template

class Plugin(BasePlugin):
	
	name         = 'shout'
	display_name = 'shout'
	requires     = ['advanced_commands']

	def on_plugin_init(self):
		# Config registers
		#self._fmt_entry = self.config.get('entry_format', "[${id}] ${clean_name}^7")
		
		# Register command
		self._cmd = Command("shout", self.command_shout, None, "!shout <message>");
		self._cmd.add_argument("text", str, "shouting text", "+");
		command_plugin = self.get_plugin("advanced_commands")
		command_plugin.register_command(self._cmd);

	# list all players
	def command_shout(self, executor, args): 
		msg = ' '.join(str(x) for x in args.text)
		for col in range(0, 5):
			self.broadcast_chat('^'+str(col) + msg)