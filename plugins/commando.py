import os
import imp
import system.globals

from system.base_plugin import BasePlugin

class Plugin(BasePlugin):
	def __init__(self):
		super(BasePlugin, self).__init__()
		
		self.name     = 'Commando'
		self.version  = '0.1a'

		self._director = "!"
		self._commands_dir = system.globals.PLUGINS_PATH + '/commando_data/'

		self._commands = []

	def on_plugin_init(self):
		self._load_commands()

	def on_player_chat(self, player, message):
		if message[0] == self._director:
			pass
		else:
			return message

	def _load_commands(self):
		for fn in os.listdir(self._commands_dir):
			file_path = self._commands_dir + fn
			file_base_name, ext = os.path.splitext(fn)

			if os.path.isfile(self._commands_dir + fn):
				# Ensure we do not hit the base command module
				if file_base_name == "base_command" or file_base_name == "__init__":
					continue

				if ext != ".py":
					continue

				# Initialize the command and push it into the stack
				f, filename, desc = imp.find_module(file_base_name, [self._commands_dir])
				command = imp.load_module(file_base_name, f, filename, desc).Command()

				self._commands.append(command)

				self.log_info("Loaded command " + command.alias)