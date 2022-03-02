import socket
#bind shell, hacker calls victim

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('10.211.55.5',4444)) #bind to this machine! 127.0.0.1 might work to? 
s.listen(0)
print('waiting for connection')
connection,address = s.accept() #address is tuple with address and port
print(connection) #connection is the socket object with information about local address and remote address
print('Connection established with ' + str(address[0]) + ' on port ' + str(address[1]))





















