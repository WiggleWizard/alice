from system.function import Function

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

	@classmethod
	def extend(self, func):
		setattr(self, func.__name__, func)

	def init(self, id, ip, guid, name):
		self._id   = id
		self._ip   = ip
		self._guid = guid
		self._name = name

	def tell(self, message):
		void_func = Function('TELL', 0, self._id, message)
		self._alice._rabbithole.send_void_func(void_func)

	def get_ip(self):
		return self._ip

	def get_id(self):
		return self._id

	def get_clean_name(self):
		return re.sub(r"\^\d", "", self._name)

	def kick(self, reason):
		void_func = Function('KICK', 0, self._id, reason)
		self._alice._rabbithole.send_void_func(void_func)