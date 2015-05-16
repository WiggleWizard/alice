from system.base_plugin import BasePlugin

from system.player import Player

class Plugin(BasePlugin):

	name         = "permissions"
	display_name = "Permissions"

	def on_plugin_init(self):
		self._extend_player()

	def on_player_dc(self, player):
		player._permissions = []


#=======================================================================================#
# Player Extension Functions                                                            #
#=======================================================================================#

	def _extend_player(self):
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