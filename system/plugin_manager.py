import json
import os
import imp

import globals
from base_plugin import BasePlugin

class PluginManager:
	def __init__(self, alice):
		self._plugin_dir = globals.PLUGINS_PATH + "/"

		self._alice = alice
		self._plugins = []

		# Load the plugin priority
		json_data = open(globals.BASE_PATH + '/plugin_priority.cfg')
		self._plugin_priority = json.load(json_data)
		json_data.close()

	##
	# Loads plugins from the Plugin folder.
	# 
	# load_plugins:
	##
	def load_plugins(self):
		for fn in os.listdir(self._plugin_dir):
			file_path = self._plugin_dir + fn
			file_base_name, ext = os.path.splitext(fn)

			if os.path.isfile(self._plugin_dir + fn):
				if ext == '.py' and file_base_name != '__init__':
					# Load up the module
					f, filename, desc = imp.find_module(file_base_name, [self._plugin_dir])
					plugin = imp.load_module(file_base_name, f, filename, desc).Plugin()

					plugin._alice = self._alice
					plugin.machine_name = file_base_name

					# Do not continue to load the plugin if it has no name
					if not hasattr(plugin, 'name'):
						print('[PluginManager][Error] Could not load ' + file_base_name + ext + ' because it does not contain the "name" attribute')
						return
					
					# Add the priority of the plugin load order to the plugin
					try:
						plugin._priority = self._plugin_priority[file_base_name]
					except KeyError:
						pass

					# Add the plugin object in to the list
					self._plugins.append(plugin)


	##
	# Sorts the loaded plugins based on their priority number.
	# 
	# prioritize_plugins:
	##
	def prioritize_plugins(self):
		self._plugins.sort(key=lambda x: x._priority)

	def initialize_plugins(self):
		for plugin in self._plugins:
			if hasattr(plugin, 'version'):
				print('[PluginManager] Initializing plugin ' + plugin.name + ' v' + plugin.version)
			else:
				print('[PluginManager] Initializing ' + plugin.name)

			if hasattr(plugin, 'on_plugin_init'):
				plugin.on_plugin_init()


	#=======================================================================================#
	# Gtors and Stors                                                                       #
	#=======================================================================================#
	
	##
	# Gets a plugin instance, mostly used to interact with a plugin or set variables.
	# 
	# get_plugin_instance:
	# 	@param  plugin_name [str]    - Plugin's machine name (Base file name)
	# 	@return             [Plugin] - Plugin instance
	##
	def get_plugin_instance(self, plugin_machine_name):
		for plugin in self._plugins:
			if plugin.machine_name == plugin_machine_name:
				return plugin


	#=======================================================================================#
	# Plugin Propagation Calls                                                              #
	#=======================================================================================#
		
	def propagate_on_server_init(self):
		for plugin in self._plugins:
			if hasattr(plugin, "on_server_init"):
				plugin.on_server_init()

	def propagate_on_join_req(self, ip, qport):
		for plugin in self._plugins:
			if hasattr(plugin, "on_join_req"):
				plugin.on_join_req(ip, qport)

	def propagate_on_player_chat(self, player, message):
		# Filter the stupid NAK character
		if message[0] == chr(0x15):
			message = message.lstrip(chr(0x15))
				
		for plugin in self._plugins:
			if hasattr(plugin, "on_player_chat"):
				if message != None and message != "":
					message = plugin.on_player_chat(player, message)
				else:
					break

	def propagate_on_player_join(self, player):
		for plugin in self._plugins:
			if hasattr(plugin, "on_player_join"):
				plugin.on_player_join(player)

	def propagate_on_player_dc(self, player):
		for plugin in self._plugins:
			if hasattr(plugin, "on_player_dc"):
				plugin.on_player_dc(player)