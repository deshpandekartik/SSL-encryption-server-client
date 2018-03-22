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
        
            	try:
                	self.ssl_sock.connect((self.host, self.port))
            	except socket.error, msg:
                    	self.printErr("Socket connection error in client: ", msg);
                    

	def send_messages(self,to_server_chat):
		self.ssl_sock.sendall(to_server_chat)

	def close_connection(self):
		self.soc.close()
                self.ssl_sock.close()


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
	client.send_messages("asdasd")
	client.close_connection()
