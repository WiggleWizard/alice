import socket
import struct
import globals

class RabbitholeInterface:
	def __init__(self):
		self._sock = None
		self._packet_buffer = []

	# Connects to the rabbit hole and stores the connection
	# locally
	def connect(self, path):
		self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

		try:
			self._sock.connect(path)
		except:
			print >> sys.stderr, msg
			sys.exit(1)

		print('[RabbitholeInterface] Connection to rabbit hole "' + path + '" successful')

	def recv(self):
		# At the beginning of each packet there's 5 bytes that describes
		# the packet type and the payload length
		rx = self._sock.recv(5)

		if len(rx) >= 5:
			# Once we recieve the payload length we then attempt to recieve the rest of the packet
			payload_len = struct.unpack('>I', rx[1:])[0]
			rx += self._sock.recv(payload_len)

			return rx
		else:
			return None

	def close(self):
		self._sock.close()

	##
	# Requests a return from Wonderland when calling a function.
	# 
	# send_return_func:
	# 	@param return_func [ReturnFunction] - Return function instance
	##
	def send_return_func(self, return_func):
		compiled = return_func.compile()

		if globals.DEBUG:
			function_name = return_func.get_function_name()
			args          = return_func.get_args()

			out = 'Sending return function: ' + function_name + '('
			out += ', '.join(map(str, args))
			print(out + ")")
			print("\t[" + ":".join("{:02x}".format(ord(c)) for c in compiled) + "]")

		self._sock.send(compiled)

		# Now we wait for a return, anything that's NOT the returning function
		# should be put into the buffer which will be dealt with after dealing
		# with the returning function.
		while True:
			packet = self.recv()

			if packet[0] == 'R':
				if globals.DEBUG:
					print("Recieved return function: ")
					print("\t[" + ":".join("{:02x}".format(ord(c)) for c in packet) + "]")

				return_func.parse(packet)
				return return_func.get_return()

			self._packet_buffer.append(packet)

	def send_void_func(self, void_func):
		compiled = void_func.compile()

		if globals.DEBUG:
			function_name = void_func.get_function_name()
			args          = void_func.get_args()

			out = "Sending void function: " + function_name + "("
			out += ', '.join(map(str, args))
			print(out + ")")
			print("\t[" + ":".join("{:02x}".format(ord(c)) for c in compiled) + "]")
		
		self._sock.send(compiled)

	