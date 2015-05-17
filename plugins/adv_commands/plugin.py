import os
import imp
import argparse
import system.globals

from system.base_plugin import BasePlugin

# Internal
CMD_STATUS_NO_CMD      = 0
CMD_STATUS_SUCCESS     = 1
CMD_STATUS_MISSING_ARG = 2
CMD_STATUS_NO_PERMS    = 3
CMD_STATUS_ARGS_TOO_LONG=4

class ArgumentParserError(Exception): pass

class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

class Command:
	def __init__(self, name, command_method, perm, hint):
		self._alias = name
		self._parser = ThrowingArgumentParser(add_help=False)
		self._command = command_method
		self._perm = perm
		self._hint = hint

	def add_argument(self, arg_name, arg_type, hint, rep=1):
		self._parser.add_argument(arg_name, type=arg_type, help=hint, nargs=rep)

	def execute(self, executor, args):
		#try:
			pargs = self._parser.parse_args(args)
			print args

			self._command(executor, pargs);
		#except ArgumentParserError as ape:
		#	executor.tell("^1Invalid command semantics: " + str(ape))

	def get_plugin(self, plugin_name):
		plugin_manager = self._alice.get_plugin_manager()
		return plugin_manager.get_plugin_instance(plugin_name)
		


class Plugin(BasePlugin):

	name         = 'advanced_commands'
	display_name = 'Advanced Commands'
	version      = '1.0'

	def __init__(self):
		self._commands = []

	def on_plugin_init(self):
		self._director = self.config.get("directive", "!")
#		self._commands_dir = system.globals.PLUGINS_PATH + '/adv_commands_data/'

	def register_command(self, cmd):
		self._commands.append(cmd)


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

		cmd_candidate = [];
		for command in self._commands:
			if command._alias == cmd_issued:
				if command._perm != None:
					if not player.has_perm(command._perm):
						return CMD_STATUS_NO_PERMS

				# Attempt to split the args according to how the command
				# specified.
				#split_max = command['argc']

				if(len(arg_string) > 100):
					return CMD_STATUS_ARGS_TOO_LONG

				args = arg_string.split(" ")

				if args[0] == "":
					args = []

				try:
					command.execute(player, args);
				except ArgumentParserError as ape:
					cmd_candidate.append(command._hint+": " + str(ape))
					continue
					#executor.tell("^1Invalid command semantics: " + str(ape))
				
				# If the command returns no status then we automatically
				# assume it handled its own output.
				cmd_result = None
				if cmd_result == None:
					cmd_result = CMD_STATUS_SUCCESS

				return cmd_result

		player.tell("^1Invalid command semantics, candidates are: " + " ".join(cmd_candidate))
		return CMD_STATUS_NO_CMD