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
			print("Command")
			message_split = message[1:].split(" ", 1)

			# If the command looks like "!" or "! command" this if statement
			# will catch this type of input.
			if message_split[0] == "":
				player.tell("^1No such command")
				return None

			cmd_issued = message_split[0]

			arg_string = None
			try:
				arg_string = message_split[1]
			except IndexError:
				pass

			found_cmd = False

			for command in self._commands:
				if command.alias == cmd_issued:
					# We attempt to execute the custom executor which
					# we assume will deal with the argument string itself
					# in its own way.
					try:
						command.execute_custom(player, arg_string)
					except AttributeError:
						# Now we split the input argument according to the command's
						# spec.
						try:

							command.execute(player)
						except AttributeError:
							self.log_info(command.alias + " does not have an execution function")
		else:
			return message

	##
	# Loads commands in commando_data into memory.
	# 
	# _load_commands:
	##
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

				# Place the alice instance into the command
				command._alice = self._alice

				self._commands.append(command)

				self.log_info("Loaded command " + command.alias)