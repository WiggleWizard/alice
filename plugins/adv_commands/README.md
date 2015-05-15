Advanced Commands
=================

Advanced Commands allows plugin makers to easily add ingame commands to their plugins.


Moderators
----------

### Config Variables

*	**`directive`**

		Type:    string
		Default: !
	
	Denotes the character required to start a command in the chat. If more than 1 character is set for this config variable, Advanced Commands will only use the first character; any subsequence characters after that will be ignored.


Developers
----------

### Methods

*	**`register_command(function, alias, argc, required_perm=None)`**

		@param function      <function>  - Pointer to the function to run when this command is executed.  
		@param alias         <string>    - Alias the command is executed as.
		@param argc          <int>       - Required arguments.  
		@param required_perm <string>

	Registers a command to execute.
	
	```
	# First get the advanced comands plugin instance
	adv_command_plugin = self.get_plugin("advanced_commands")
	# Register the command
	adv_command_plugin.register_command(self.command_example, "example", 0)
	```
	
	Do note that the `function` bound does not have to have `command_` prepended. This is personal preferrence. The function/method name can be any function pointer.