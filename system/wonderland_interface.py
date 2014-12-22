import socket
import sys
import struct

class WonderlandInterface:
	def __init__(self):
		pass

	def request_rabbithole(self, suffix):
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

		try:
			sock.connect('/tmp/wonderland-' + suffix)
		except:
			print >> sys.stderr, msg
			sys.exit(1)

		print('[WonderlandInterface] Connection to Wonderland successful')

		# Send out a rabbit hole request
		payload = 'RABBITHOLE'

		packet  = struct.pack('>I', 1)
		packet += struct.pack('>I', len(payload))
		packet += payload

		sock.send(packet)

		print('[WonderlandInterface] Request for rabbit hole sent')

		# Attempt to receive the rabbit hole path
		rx = sock.recv(512)
		print('[WonderlandInterface] Rabbit hole at "' + rx[4:] + '"')

		sock.close()
		
		return rx[4:]
