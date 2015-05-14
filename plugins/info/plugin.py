from system.base_plugin import BasePlugin

from system.player import Player

class Plugin(BasePlugin):
	
	name         = 'info'
	display_name = 'info'
	requires     = ['advanced_commands']

	def on_plugin_init(self):
		# Register command
		command_plugin = self.get_plugin("advanced_commands")
		command_plugin.register_command(self.command_p, 'p', 0);

	# list all players
	def command_p(self, executor, args): 
		if(len(args) > 1):
			executor.tell('^1Wrong number of parameters!')
			return

		if(len(args) > 0):
			try:
				page = int(args[0])
				if(page < 0):
					executor.tell('^1Parameter needs to be a number >=0')
					return
			except ValueError:
				executor.tell('^1Parameter needs to be a number >=0')
				return
			
			i = 0
			page = int(args[0])
			for player in self._alice._players: # print a page of 5 players
				if player != None:
					if i >= page*5 and i < (page+1)*5:
						executor.tell(str(player.get_id())+"|"+player.get_clean_name()+"|"+player.get_ip())
					i+=1
		else:
			for player in self._alice._players: # print all, no parameter
				if player != None:
					executor.tell(str(player.get_id())+"|"+player.get_clean_name()+"|"+player.get_ip())

	
		
