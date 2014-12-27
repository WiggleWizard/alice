import re

class Player:
	def __init__(self, alice):
		self._alice = alice
		self._id    = -1
		self._ip    = None
		self._name  = None
		self._guid  = None

	def __str__(self):
		return "[" + str(self._id) + "] " + self._name

	def init(self, id, ip, guid, name):
		self._id   = id
		self._ip   = ip
		self._guid = guid
		self._name = name

	def tell(self, message):
		self._alice.tell(self._id, message)

	def get_ip(self):
		return self._ip

	def get_clean_name(self):
		return re.sub(r"\^\d", "", self._name)