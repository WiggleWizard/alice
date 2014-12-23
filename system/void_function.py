import struct

import globals

class VoidFunction:
	def __init__(self, function_name, a1=None, a2=None, a3=None):
		self._args = []

		if a1 != None:
			self._args.append(a1)
		if a2 != None:
			self._args.append(a2)
		if a3 != None:
			self._args.append(a3)

		self._func_name = function_name

	def compile(self):
		# Determine the payload size while constructing the payload
		# itself
		sz = 0
		payload = ''

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

		packet = 'V' + struct.pack('>I', len(payload)) + payload

		return packet

	def get_args(self):
		return self._args

	def get_function_name(self):
		return self._func_name