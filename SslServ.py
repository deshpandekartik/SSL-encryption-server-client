import time
import threading
import socket
import ssl
import sys
import hashlib
from TCPBase import TCPBase

class SSLServer(TCPBase):
    
	host = None
	port = None
	ssl_keyfile = None
	ssl_certfile = None
	BUFFERSIZE = 1024
	credentials = {}

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
			sys.exit(0)
            
		try:
                	self.soc.listen(10)
            	except socket.error, msg:
                	print "Listen failed: "  + str(msg[0]) + " Message " + msg[1]
			sys.exit(0)           
 
		self.handle_requests() 
        
		self.exit_server()

	def exit_server(self):
		self.soc.close()
                self.connstream.close()
                print "exit server"

	def update_users(self):
		self.credentials = {}
		with open ('password', 'r') as file:
	        	for line in file:
        	        	split = line.split()
                		self.credentials[split[0]] = split[1]	

		return self.credentials


	def handle_requests(self):
		while True:
	                self.conn, self.addr = self.soc.accept()
        	        try:
                	        self.connstream = ssl.wrap_socket(self.conn,
                                                  server_side=True,
                                                  certfile=self.ssl_certfile,
                                                  keyfile=self.ssl_keyfile,
                                                  ssl_version=ssl.PROTOCOL_TLSv1
                                                  )
                	except socket.error, msg:
                                print "SSL wrap failed for server: "  + str(msg[0]) + " Message " + msg[1]
                                sys.exit(0)

                        userid = self.connstream.recv(self.BUFFERSIZE)
			rawpassword = self.connstream.recv(self.BUFFERSIZE)	

			password = hashlib.md5(rawpassword.encode()).hexdigest()

			print "UserID : " + str(userid) + " Password : " + str(rawpassword) + " Hashed Passsowrd : " + str(password) 

			self.credentials = self.update_users()

			if userid in self.credentials:
				if self.credentials[userid] == password:
					to_client = "OK"
				else:
					to_client = "the password is incorrect"
			else:
				to_client = "the password is incorrect"
			
			self.conn.sendall(to_client)

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
