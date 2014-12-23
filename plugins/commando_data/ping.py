from plugins.commando_data.base_command import BaseCommand

class Command(BaseCommand):
	def __init__(self):
		self.alias       = "ping"
		self.description = "Invokes a response from Alice"
		self.args        = 0

	def execute(self, executor, args, argc):
		pass