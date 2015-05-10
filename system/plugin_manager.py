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

	def load_plugins(self):
		for fn in os.listdir(self._plugin_dir):
			file_path = self._plugin_dir + fn

			if os.path.isdir(file_path) and os.path.isfile(file_path + '/plugin.py'):
					self._setup_plugin(file_path)

	def _setup_plugin(self, plugin_folder_path):
		folder_name = os.path.basename(plugin_folder_path)

		# Load up the module
		f, filename, desc = imp.find_module("plugin", [plugin_folder_path])
		plugin = imp.load_module("plugin", f, filename, desc).Plugin()

		# If there is no code_name in the plugin, then we set the
		# code_name according to the folder name that it's in.
		if not hasattr(plugin, 'name'):
			print(
				'[PluginManager][Warning] "' + folder_name +
				'" plugin has no "code_name" attribute. '
				'Using the plugin\'s folder name as the code_name'
			)
			plugin.name = folder_name

		# Same thing as above but for the friendly name
		if not hasattr(plugin, 'display_name'):
			print(
				'[PluginManager][Warning] Could not load ' + plugin.name +
				' because it does not contain the "name" attribute'
			)
			plugin.display_name = plugin.name

		plugin._alice = self._alice
		
		# Add the priority of the plugin load order to the plugin
		try:
			plugin._priority = self._plugin_priority[plugin.name]
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
				print('[PluginManager] Initializing plugin ' + plugin.display_name + ' v' + plugin.version)
			else:
				print('[PluginManager] Initializing ' + plugin.display_name)

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
	def get_plugin_instance(self, plugin_name):
		for plugin in self._plugins:
			if plugin.name == plugin_name:
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