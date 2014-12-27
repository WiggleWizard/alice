r"""
	database_ext
	~~~~~~~~~~~~

	Designed to interact with Sigil, however it can be modified
	to work with even an SQLite stack if required. Ensure you
	rework database.py too in order to correct connection
	information.
"""

from system.base_plugin import BasePlugin

from system.player import Player

from libs.phpserialize import *

class Plugin(BasePlugin):
	def __init__(self):
		super(BasePlugin, self).__init__()

		self.name    = "Permissions"
		self.version = "1.0"
		self.require = "database"

	def on_plugin_init(self):
		# Player variable extensions
		Player._perms            = []
		Player._is_logged_in     = False
		Player._sigil_id         = 0
		Player._sigil_username   = None
		Player._sigil_group_name = None
		Player._sigil_group_rank = 0

		# Player function extensions
		Player.has_perm               = None
		Player.set_perms              = None
		Player.retrieve_sigil_id      = player_retrieve_sigil_id
		Player.retrieve_sigil_details = player_retrieve_sigil_details


#=======================================================================================#
# Player Extension Functions                                                            #
#=======================================================================================#

def player_has_perm(self, perm):
	return perm in self._perms

##
# Gets the Sigil ID of the player by his IP address and sets variables
# in the player instance.
# 
# player_retrieve_sigil_id:
# 	@return [bool] - True if the ID was successfully retrieved
##
def player_retrieve_sigil_id(self):
	sql = """
		SELECT
			last_activity,
			user_data
		FROM
			sessions
		WHERE
			ip_address=%s
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

##
# Retrieves Sigil details from the database and sets variables 
# in the player instance.
# 
# player_retrieve_sigil_details:
##
def player_retrieve_sigil_details(self):
	if self._is_logged_in == True:
		sql = """
			SELECT
				accounts.id AS user_id,
				accounts.username AS username,
				accounts.ingame_name AS ingame_name,

				`groups`.name AS group_name,
				`groups`.rank AS group_rank,

				perm_keys.key AS perm_key
			FROM
				accounts
			LEFT JOIN
				account_groups ON (account_id=accounts.id)
			LEFT JOIN
				`groups` ON (account_groups.group_id=`groups`.id)
			LEFT JOIN
				alice_perms ON (`group`=account_groups.group_id)
			LEFT JOIN
				perm_keys ON (perm_keys.id=alice_perms.perm_key_id)
			WHERE accounts.id=%s
		"""

		self.db_cursor.execute(sql, [self._sigil_id])
		data = self.db_cursor.fetchall()

		# We only need to loop through the perms, so we just grab the first
		# entry and get the data off that
		self._sigil_id         = int(data[0][0])
		self._sigil_username   = data[0][1] # Username, not friendly name
		self._sigil_group_rank = int(data[0][4])
		self._sigil_group_name = data[0][3]

		# Now we loop through the set and get the perms
		for entry in data:
			self._perms.append(entry[5])