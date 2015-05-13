from system.base_plugin import BasePlugin

from system.player import Player

class Plugin(BasePlugin):
	
	name         = 'phpbb_autologin'
	display_name = 'PHPBB Autologin'
	version      = '1.0'
	requires     = ['database']

	def on_plugin_init(self):
		self._extend_player()

		# Get the database plugin instance and ensure that
		# we can access the DB cursor from this plugin.
		db_plugin = self.get_plugin("database")
		self._db_cursor = db_plugin._db_cursor

	def _extend_player(self):
		# Variables
		Player._phpbb_is_logged_in = False
		Player._phpbb_id           = 0
		Player._phpbb_username     = ""
		Player._phpbb_group_name   = ""
		Player._phpbb_group_id     = 0

	def on_player_join(self, player):
		# When a player joins, the plugin will poll the PHPBB
		# database with the player's IP and gets the player's
		# PHPBB data.
		sql = """
			SELECT
				last_activity,
				user_data
			FROM
				sessions
			WHERE
				ip_address = %s
			ORDER BY last_activity DESC
		"""
		self.db_cursor.execute(sql, [self._ip])
		data = self.db_cursor.fetchone()

		# Decode the data that's stored by Sigil in the database
		if data:
			user_data  = loads(data[1])

			if "account_id" in user_data:
				self._sigil_id     = int(user_data['account_id'])
				self._is_logged_in = True
				return True

		return False