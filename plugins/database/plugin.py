from system.base_plugin import BasePlugin

import MySQLdb

from system.player import Player

class Plugin(BasePlugin):
	
	name         = "database"
	display_name = "Database Connector"
	version      = "1.0"
	
	def __init__(self):
		self._db     = None
		self._cursor = None

	def on_plugin_init(self):
		self.log_info("Database connecting")
		self._db = MySQLdb.connect(host=   self.config.get('host', "localhost"),
								   user=   self.config.get('user', "root"),
								   passwd= self.config.get('password', ""),
								   db=     self.config.get('database', ""))
		self.log_info("Connection successful")

		self._cursor = self._db.cursor()
		
		# Allow player instances access to the database
		Player.db_cursor = self._cursor

	def get_cursor(self):
		return self._cursor