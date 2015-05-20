from system.base_plugin import BasePlugin

class Command(object):

	CMD_STATUS_NO_CMD         = 0
	CMD_STATUS_SUCCESS        = 1
	CMD_STATUS_MISSING_ARG    = 2
	CMD_STATUS_NO_PERMS       = 3
	CMD_STATUS_ARGS_TOO_LONG  = 4
	CMD_STATUS_ARGS_TOO_SHORT = 5
	CMD_STATUS_ARG_PARSE_ERROR = 6

	def __init__(self, aliases, func, perm):
		self._aliases = aliases
		self._func    = func
		self._perm    = perm

		self._parameters       = []
		self._mandatory_params = 0
		self._optional_params  = 0
		self._has_free_text        = False
		
	def add_param(self, name, parse_method, hint, description, optional=False):
		self._parameters.append({
			'name': name,
			'parse_method': parse_method,
			'hint': hint,
			'description': description
		})

		if optional:
			self._optional_params++
		else
			self._mandatory_params++

	def has_free_text(self, b=True):
		self._has_free_text = b

	def param_count(self):
		return len(self._parameters)

	def mandatory_param_count(self):
		return self._mandatory_params

	def optional_param_count(self):
		return self._optional_params


class Plugin(BasePlugin):

	name         = 'advanced_commands'
	display_name = 'Advanced Commands'
	version      = '2.0a'

	def on_plugin_init(self):
		self._commands = []
		self._director = self.config.get("directive", "!")

	def register_command(self, aliases, func, perm):
		cmd = Command(aliases, func, perm)
		self._commands.append(cmd)

		return cmd

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
				elif cmd_result == CMD_STATUS_ARGS_TOO_LONG:
					player.tell("^1Argument string too long")
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
			# Commands can have multiple aliases, so we check for them here
			if cmd_issued in command._aliases:
				# If the player doesn't have the perms then move on
				if command._perm != None and not player.has_perm(command._perm):
					return CMD_STATUS_NO_PERMS

				args_list = []
				free_text = None

				# Break the input arg string into free text and actual args
				arg_str_split = arg_string.split(":")
				s = len(arg_str_split)

				if s > 0:
					args_list = arg_str_split[0].trim().split(" ")
				if s = 2:
					free_text = arg_str_split[1].trim()

				# If the amount of arguments parsed does not match the required
				# amount of args the command requires then send an error.
				if len(args_list) < command.mandatory_param_count():
					return Command.CMD_STATUS_ARGS_TOO_SHORT
				if len(args_list) > command.param_count():
					return Command.CMD_STATUS_ARGS_TOO_LONG

				# Loop through the parameters of the command and add each
				# one to the dictionary and call the parsing function
				# on each one too.
				args = {}
				i = 0
				for arg in args_list:
					r = command._parameters[i].parse_method(arg)

					if not r:
						return Command.CMD_STATUS_ARG_PARSE_ERROR

					args[command._parameters[i].name] = r
					
					i++

				try:
					command.execute(player, args);
				
				# If the command returns no status then we automatically
				# assume it handled its own output.
				cmd_result = None
				if cmd_result == None:
					cmd_result = CMD_STATUS_SUCCESS

				return cmd_result
		return CMD_STATUS_NO_CMD

	def param_parse_player_search(self, search):
		return []