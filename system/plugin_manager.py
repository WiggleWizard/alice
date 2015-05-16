import json
import os
import imp

import globals
from system.plugin_config import PluginConfig
import ConfigParser

class PluginManager:
	def __init__(self, alice):
		self._alice   = alice
		self._plugins = []

		self._plugin_groups   = self._get_plugin_groups()
		self._plugin_priority = self._get_priority_list()

	##
	# Reads the keys and values from the general config and inserts the keys as
	# a key in the dictionary and inserts the absolute path of the value of each key
	# into the value of the dictionary.
	##
	def _get_plugin_groups(self):
		rtn = {}
		rtn['default'] = os.path.abspath("plugins")

		try:
			# Loop through all the dirs defined in the config and get all the paths
			config_items = self._alice._alice_config.items("plugin_groups")
			for key, value in config_items:
				# We have already provided the plugins directory as default
				# so we don't need duplicates.
				if value != 'plugins':
					rtn[key] = os.path.abspath(value)
		except ConfigParser.NoSectionError:
			pass

		return rtn

	def _load_plugin_group(self, group, group_path):
		dir_list = os.listdir(group_path)
		for fd in dir_list:
			plugin_path = group_path + "/" + fd

			if os.path.isdir(plugin_path) and os.path.isfile(plugin_path + '/plugin.py'):
				self._setup_plugin(plugin_path)

	##
	# Correctly sets up a plugin, adding necessary attributes to the plugin
	# making it easier to write a plugin without having to write a bunch of
	# predetermined code.
	# 
	# _setup_plugin:
	# 	@param  plugin_path [str] - Full path to the plugin's containing folder.
	##
	def _setup_plugin(self, plugin_path):
		folder_name = os.path.basename(plugin_path)

		# Load up the module
		f, filename, desc = imp.find_module("plugin", [plugin_path])
		plugin = imp.load_module("plugin", f, filename, desc).Plugin()

		# If there is no code_name in the plugin, then we set the
		# code_name according to the folder name that it's in.
		if not hasattr(plugin, 'name'):
			print(
				'[PluginManager][Warning] Plugin "' + plugin.name +
				'" has no name, using the plugin\'s folder name'
			)
			plugin.name = folder_name

		# Same thing as above but for the friendly name
		if not hasattr(plugin, 'display_name'):
			print(
				'[PluginManager][Warning] Plugin "' + plugin.name +
				'" has no display name, using the plugin\'s name'
			)
			plugin.display_name = plugin.name

		plugin._alice = self._alice

		# Create a new config object for this plugin
		plugin.config = PluginConfig(self._alice._plugin_config, plugin)
		
		# Add the priority of the plugin load order to the plugin
		if plugin.name in self._plugin_priority:
			plugin._priority = self._plugin_priority[plugin.name]
			self._plugins.append(plugin)
		else:
			print "Plugin " + plugin.name + " is disabled, add priority to enable it"

	##
	# Sorts the loaded plugins based on their priority number.
	# 
	# prioritize_plugins:
	##
	def prioritize_plugins(self):
		self._plugins.sort(key=lambda x: x._priority)

	##
	# Usually called after the plugins are loaded into memory.
	# 
	# initialize_plugins:
	##
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

	def _get_priority_list(self):
		rtn = {}

		config_items = self._alice._alice_config.items("plugin_priority")
		for key, value in config_items:
			rtn[key] = int(value)

		return rtn

	def load_plugins(self):
		plugin_groups = self._plugin_groups.items()
		for group, group_path in plugin_groups:
			# Check to see if the pugin group's path exists
			if os.path.isdir(group_path):
				self._load_plugin_group(group, group_path)
			else:
				print(
					"[PluginManager][Warning] Failed to load plugin group '" + group +
					"' because the group's path (" + group_path + 
					") does not exist"
				)


	#=======================================================================================#
	# Custom Plugin Propagation Calls                                                              #
	#=======================================================================================#
	
	def propagate_event(self, event, params):
		for plugin in self._plugins:
			if hasattr(plugin, event):
				plugin[event](*params)


	#=======================================================================================#
	# Alice Plugin Propagation Calls                                                              #
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
