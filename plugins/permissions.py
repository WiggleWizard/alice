from system.base_plugin import BasePlugin

from system.player import Player

class Plugin(BasePlugin):
	def __init__(self):
		super(BasePlugin, self).__init__()

		self.name    = "Permissions"
		self.version = "1.0"
		self.require = "database"

		Player._perms         = []
		Player.has_perm       = None
		Player.set_perms      = None
		Player.retrieve_perms = None