from system.base_plugin import BasePlugin

from system.player import Player

class Plugin(BasePlugin):

	name         = "permissions"
	display_name = "Permissions"

	def on_plugin_init(self):
		Player._permissions = []

	@Player.extend
	def has_permission(self, permission):
		return permission in self._permissions

	@Player.extend
	def set_permissions(self, permissions=[]):
		if type(permissions) == list:
			self._permissions = permissions

	@Player.extend
	def get_permissions(self):
		return self._permissions