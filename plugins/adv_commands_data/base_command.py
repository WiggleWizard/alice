class BaseCommand:
	def broadcast_chat(self, message):
		self._alice.broadcast_chat(message)

	def find_players_by_partial(self, partial_name):
		return self._alice.find_players_by_partial(partial_name)