from system.base_plugin import BasePlugin

from system.player import Player

class Plugin(BasePlugin):
	
	name         = 'phpbb_autologin'
	display_name = 'PHPBB Autologin'
	version      = '1.0'
	requires     = ['database']

	def on_plugin_init(self):
		# Get the table names
		# TODO: Prepared statements wrap quotes around strings when formatting
		#       so table names in a prepared statement won't work. For obvious reasons.
		#self._table_sessions = self.config.get('session_table', 'phpbb_sessions')
		#self._table_users    = self.config.get('users_table', 'phpbb_users')

		self._extend_player()

		# Get the database plugin instance and ensure that
		# we can access the DB cursor from this plugin.
		db_plugin = self.get_plugin("database")
		self._db_cursor = db_plugin._cursor

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
				session_user_id
			FROM
				phpbb_sessions
			WHERE
				session_ip = %s
		"""
		self._db_cursor.execute(sql, [player.get_ip()])
		data = self._db_cursor.fetchone()

		# Decode the data that's stored by PHPBB in the database
		if data:
			player._phpbb_is_logged_in = True
			player._phpbb_id = data['session_user_id']