import socket
from udp_send.py import server_address, server_port

def set_udp():
	# Set up UDP
	udp_marker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	message1 = 0 #"Trial Start"
	message2 = 100 #"Button press match"
	message3 = 200 #"Button press no-match"
	message4 = 300 #"Timeout"
	message5 =  400 #"Trial End"
	message6 = '1' 
	message7 = '2' 
	ip = server_address
	port = server_port
	
	return None
	
