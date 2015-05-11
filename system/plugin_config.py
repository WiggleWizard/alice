class PluginConfig(self):
	def __init__(self, config, plugin):
		self._plugin = plugin



	def get(self, variable_name, default=None):
