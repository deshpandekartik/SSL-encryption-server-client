import time
import threading
import socket
import ssl
import sys
from TCPBase import TCPBase

class SSLServer(TCPBase):
    
	host = None
	port = None
	ssl_keyfile = None
	ssl_certfile = None

	def __init__(self, host_arg, port_arg, ssl_keyfile_arg, ssl_certfile_arg):
		self.host = "localhost"
		self.port = port_arg
		self.ssl_keyfile = ssl_keyfile_arg
		self.ssl_certfile = ssl_certfile_arg
        	super(SSLServer, self).__init__()
       
    	def start_server(self):
        	err = 0
        	msg = None
        	try:
        		self.soc.bind((self.host, self.port))
        	except socket.error , msg:
            		print "Bind failed in server: " + str(msg[0]) + " Message " + msg[1]
            
		try:
                	self.soc.listen(10)
            	except socket.error, msg:
                	print "Listen failed: "  + str(msg[0]) + " Message " + msg[1]
            
		self.conn, self.addr = self.soc.accept()
            	try:
                	self.connstream = ssl.wrap_socket(self.conn, 
                                                  server_side=True,
                                                  certfile=self.ssl_certfile,
                                                  keyfile=self.ssl_keyfile, 
                                                  ssl_version=ssl.PROTOCOL_TLSv1
                                                  )
            	except socket.error, msg:
                	if (msg != None) :
                    		print "SSL wrap failed for server: "  + str(msg[0]) + " Message " + msg[1]
           
		self.handle_requests() 
        
		self.exit_server()

	def exit_server():
		self.soc.close()
                self.connstream.close()
                print "exit server"

	def handle_requests(self):
		while True:
                        data = self.connstream.recv(1024)
                        if data:
                                print "server: " + data



if __name__ == '__main__':
	
	if len(sys.argv) != 2:
                print "Invalid Parameters: Specify <port number>"
                sys.exit(0)
        else:
                port_arg = int(sys.argv[1])
                host_arg = socket.gethostbyname(socket.gethostname())
		ssl_keyfile_arg = "certs/ssl_key"
		ssl_certfile_arg = "certs/ssl_cert"

	print('Starting SSL Server on ' + str(host_arg) + ':' + str(port_arg) + '...')

    	server = SSLServer(host_arg,port_arg,ssl_keyfile_arg,ssl_certfile_arg)
    	server.start_server()
