import os
import imp
import system.globals

from system.base_plugin import BasePlugin

# Internal
CMD_STATUS_NO_CMD      = 0
CMD_STATUS_SUCCESS     = 1
CMD_STATUS_MISSING_ARG = 2
CMD_STATUS_NO_PERMS    = 3

class Plugin(BasePlugin):

	name         = 'advanced_commands'
	display_name = 'Advanced Commands'
	version      = '0.1a'

	def on_plugin_init(self):
		self._director = self.config.get("directive", "!")
		self._commands_dir = system.globals.PLUGINS_PATH + '/adv_commands_data/'

		self._commands = []

	def register_command(self, function, alias, argc, required_perm=None):
		self._commands.append({
			'function':      function,
			'alias':         alias,
			'argc':          argc,
			'required_perm': required_perm
		})

	##
	# Triggered when a player chats.
	# 
	# on_player_chat:
	# 	@param player  [Player] - The player instance that sent the message
	# 	@param message [str]    - The message that was sent
	##
	def on_player_chat(self, player, message):
		if message[0] == self._director:
			cmd_issued, arg_string = self._parse_message(message[1:])

			# If the command given was in the correct semantical structure
			if cmd_issued:
				cmd_result = self._attempt_exec(player, cmd_issued, arg_string)

				if cmd_result == CMD_STATUS_NO_CMD:
					player.tell("^1No such command")
				elif cmd_result == CMD_STATUS_NO_PERMS:
					player.tell("^1You do not have permission to execute this command")
			else:
				player.tell("^1Invalid command semantics")
		else:
			return message

	##
	# Parses the message into command and arg string.
	# 
	# _parse_message:
	# 	@param  message [str] - Input string, without director
	# 	@return         [str] - Command without director. Will return None if
	# 							the command semantics are incorrect.
	# 	@return         [str] - Entire string after command. Will return None
	# 							if no args are given.
	##
	def _parse_message(self, message):
		message_split = message.split(" ", 1)

		# If the command looks like "!" or "! command" this if statement
		# will catch this type of input.
		cmd_issued = None
		if message_split[0] != "":
			cmd_issued = message_split[0]

		arg_string = ""
		if len(message_split) > 1:
			arg_string = message_split[1]

		return cmd_issued, arg_string

	##
	# Attemps to execute the input command and if there's a command to execute
	# the args are passed to the command.
	# 
	# _attempt_exec:
	# 	$param  player     [Player] - Executor
	# 	$param  cmd_issued [str]    - Command
	# 	$param  arg_string [str]    - Full argument string
	# 	$return            [int]    - See CMD_STATUS_... for returns
	##
	def _attempt_exec(self, player, cmd_issued, arg_string):
		for command in self._commands:
			if command['alias'] == cmd_issued:
				if command['required_perm'] != None:
					if not player.has_perm(command['required_perm']):
						return CMD_STATUS_NO_PERMS

				# Attempt to split the args according to how the command
				# specified.
				split_max = command['argc']

				args = arg_string.split(" ", split_max)

				if args[0] == "":
					args = []

				# If the amount of args that came from the arg splitting
				# code doesn't match the number of expected args from
				# the command then just return a status.
				if command['argc'] != 0 and len(args) != command['argc']:
					return CMD_STATUS_MISSING_ARG

				# When executing the function attached to the command, we
				# give the function chance to return a status that will
				# then result in a generic response from this plugin.
				cmd_result = command['function'](player, args)

				# If the command returns no status then we automatically
				# assume it handled its own output.
				if cmd_result == None:
					cmd_result = CMD_STATUS_SUCCESS

				return cmd_result

		return CMD_STATUS_NO_CMD