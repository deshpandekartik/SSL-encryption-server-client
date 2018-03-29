openssl genrsa 1024 > ssl_key	# generate private keys
openssl req -new -x509 -nodes -sha1 -days 365 -key ssl_key > ssl_cert	# generate public key from private key
