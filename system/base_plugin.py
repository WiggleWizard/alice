class BasePlugin(object):
	
	_priority = 99

	def __init__(self):
		pass

	def log_info(self, message):
		print("[" + self.name + "][Info] " + message)

	def accept_ip(self, ip, qport):
		self._alice.accept_ip(ip, qport)

	def deny_ip(self, ip, qport, message):
		self._alice.deny_ip(ip, qport, message)

	def broadcast_chat(self, message):
		self._alice.broadcast_chat(message)