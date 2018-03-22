import time
import threading
import socket
import ssl
import sys
from TCPBase import TCPBase

class SSLClient(TCPBase):

	host = None
        port = None
        ssl_certfile = None
	BUFFERSIZE = 1024

    	def __init__(self, host_arg, port_arg, ssl_certfile_arg):
		self.host = host_arg
                self.port = port_arg
                self.ssl_certfile = ssl_certfile_arg		
        	super(SSLClient, self).__init__()
        
    	def connect_to_server(self):
        	try:
            		self.ssl_sock = ssl.wrap_socket(self.soc,
                                            ca_certs=self.ssl_certfile,
                                            cert_reqs=ssl.CERT_REQUIRED )

        	except socket.error:
            		print "SSL socket wrapping failed"
			sys.exit(0)
        
            	try:
                	self.ssl_sock.connect((self.host, self.port))
            	except socket.error, msg:
                    	print "No server found on: " + self.host + ":" + str(self.port) 
			sys.exit(0)
                    

	def send_messages(self,to_server_chat):
		self.ssl_sock.sendall(to_server_chat)

	def close_connection(self):
		self.soc.close()
                self.ssl_sock.close()

	def receive_messages(self):
		reply = self.ssl_sock.recv(self.BUFFERSIZE)
		print reply
		print self.ssl_sock


if __name__ == '__main__':

        if len(sys.argv) != 3:
                print "Invalid Parameters: Specify <host> <port number>"
                sys.exit(0)
        else:
                port_arg = int(sys.argv[2])
                host_arg = sys.argv[1]
                ssl_certfile_arg = "certs/ssl_cert"

	client = SSLClient(host_arg,port_arg,ssl_certfile_arg)
	client.connect_to_server()
	userid = raw_input("\nPlease enter User ID:\n")
	userid = userid.strip()
	password = raw_input("\nPlease enter password for User " + userid + ":\n")

	client.send_messages(userid)
	client.send_messages(password)
	client.receive_messages()

	client.close_connection()
