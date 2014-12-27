from plugins.adv_commands_data.base_command import BaseCommand

class Command(BaseCommand):
	def __init__(self):
		self.alias       = "ping"
		self.description = "Invokes a response from Alice"
		self.args        = 0

	def execute(self, executor, args):
		executor.tell("Pong")