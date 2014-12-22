import struct

class EventParser:
	def __init__(self):
		pass

	def parse(self, packet):
		if packet[0] == 'E':
			e = Event()

			# Cursor position
			cursor = 1

			packetSize = struct.unpack('>I', packet[cursor:cursor+4])
			cursor += 4

			event_name_size = struct.unpack('>I', packet[cursor:cursor+4])
			cursor += 4
			e.set_name(packet[cursor:cursor + event_name_size[0]])
			cursor += event_name_size[0]

			argc = struct.unpack('>I', packet[cursor:cursor + 4])[0]
			cursor += 4

			for i in range(argc):
				argt = struct.unpack('>b', packet[cursor:cursor + 1])[0]
				cursor += 1

				if argt == 1 or argt == 2:
					e.add_arg(struct.unpack('>I', packet[cursor:cursor + 4])[0])
					cursor += 4
				elif argt == 3:
					s = struct.unpack('>I', packet[cursor:cursor + 4])[0]
					cursor += 4
					
					e.add_arg(packet[cursor:cursor+s])
					cursor += s

			return e
		return None

class Event:
	def __init__(self):
		self.argv = []

	def set_name(self, name):
		self.name = name

	def add_arg(self, argv):
		self.argv.append(argv)

	def get_name(self):
		return self.name

	def get_arg(self, index):
		return self.argv[index]