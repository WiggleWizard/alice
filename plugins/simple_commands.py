r"""
	simple_commands
	~~~~~~~~~~~~~~~

	A simple command creator designed for dummies who just want
	to be able to make simple commands. If you are looking for
	an advanced commands creator, check out adv_commands plugin.

	Usage
	=====

	Edit the "commands.cfg" file inside the simple_commands_data
	directory. See below for examples and lexical inputs/commands.

	Lexical Input
	=============

	Lexical Input are the macros that work as inputs for commands.

	PLAYER_ID:           Player ID.
	NAME_SEARCH:         Name search, case insensitive.
	NAME_SEARCH_CS:      Name search, case sensitive.
	TEXT:                Just text.

	Lexical Commands
	================

	Lexical Commands are the macro commands used to execute a specific
	function/functionality.

	ban {PLAYER_ID}:
	kick:
	setname:
	bcastchat:    Broadcast chat message to all players.
	tell:

	Examples
	========

	The syntax for creating commands is in the form of:
	
	[perm]Lexical Command {LEXICAL_INPUT}...=command output {1}...

	[ban]ban <PLAYER_ID/NAME_SEARCH> <TEXT>=ban <1> <2>
	    !ban 14                      wh    =ban 14  wh
	Where the command requires the ban permission.


"""

from system.base_plugin import BasePlugin

class Plugin(BasePlugin):
	def __init__(self):
		super(BasePlugin, self).__init__()

		self.name = "Simple Commands"