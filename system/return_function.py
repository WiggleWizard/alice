import struct

import globals

class ReturnFunction:
	def __init__(self, function_name, packet_id, a1=None, a2=None, a3=None):
		self._return = None
		self._args = []

		if a1:
			self._args.append(a1)
		if a2:
			self._args.append(a2)
		if a3:
			self._args.append(a3)

		self._func_name = function_name
		self._packet_id = packet_id

	def compile(self):
		# Determine the payload size while constructing the payload
		# itself
		sz = 0
		payload = ''

		# - Packet ID
		sz += 4
		payload += struct.pack('>I', self._packet_id)
		# - Function name length
		sz += 4
		payload += struct.pack('>I', len(self._func_name))
		# - Function name
		sz += len(self._func_name)
		payload += self._func_name
		# - Arg count
		sz += 1
		payload += struct.pack('>b', len(self._args))
		# - Args
		for arg in self._args:
			# -- Arg type and arg
			if type(arg) is int:
				sz += 1
				payload += '\x01'
				sz += 4
				payload += struct.pack('>I', arg)
			elif type(arg) is str:
				length = len(arg)

				sz += 1
				payload += '\x03'
				sz += 4
				payload += struct.pack('>I', length)
				sz += length
				payload += arg

		packet = 'R' + struct.pack('>I', len(payload)) + payload

		return packet

	def parse(self, packet):
		if packet[0] == 'R':
			# Cursor position
			cursor = 1
			cursor += 4
			cursor += 4

			return_type = struct.unpack('>b', packet[cursor:cursor + 1])[0]
			cursor += 1

			if return_type == 1 or return_type == 2:
				self._return = struct.unpack('>I', packet[cursor:cursor + 4])[0]
			elif return_type == 3:
				s = struct.unpack('>I', packet[cursor:cursor + 4])[0]
				cursor += 4
				
				self._return = packet[cursor:cursor+s]

	def get_args(self):
		return self._args

	def get_return(self):
		return self._return

	def get_function_name(self):
		return self._func_name