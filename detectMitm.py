#!/usr/bin/python3


import scapy.all as sc
from scapy.layers import http
from loadingSpinner import spinner
import sys, subprocess, time
import threading


class fc:
        rw = '\033[31;107m'
        r = '\033[38;5;196m'
        pv = '\033[38;5;206;48;5;57m'
        end = '\033[0m'
        pink = '\033[38;5;206m'
        y = '\033[0;33;40m'
        purple = '\033[0;35m'
        cyan = '\033[36m'
        g = '\033[38;5;154m'
        b = '\033[38;5;45m'


def getMac(address):
    request = sc.ARP(pdst = address)
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    request_broadcast = broadcast/request        
    answered_list= sc.srp(request_broadcast,timeout = 5,verbose=False)[0]
    return answered_list[0][1].hwsrc


def sniff(interface='eth0'):
    sc.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    

def get_gateway():
    pipecmd = "/sbin/ip route | awk '/default/ { printf $3 }'"
    out = subprocess.check_output(pipecmd,shell=True)
    out_decode = out.decode('utf-8')
    return out_decode


def process_sniffed_packet(pkt):
    if pkt.haslayer(sc.ARP) and pkt[sc.ARP].op == 2: 
        #print(pkt.show())
        try:
            gatewayMac = getMac(get_gateway())
            realMac = getMac(pkt[sc.ARP].psrc) 
            responseMac = pkt[sc.ARP].hwsrc
            if realMac != responseMac:
                print(f'{fc.pv}[+]{fc.end} {fc.r}Unmatched ARP response caught! You are being attacked!{fc.end}')
                print(pkt.show())
        except IndexError:
            pass #fix for index error when getMac does not return anything       


spinnerRun = threading.Thread(target = spinner,args=(1,))

try:
    spinnerRun.start()
    print('Starting ARP spoof detection.')
    print(f'Gateway ARP; IP:{fc.g}{get_gateway()}{fc.end}; MAC:{fc.g}{getMac(get_gateway())}{fc.end}')
    sniff()


except Exception as e:
        print(f'\tError: {fc.rw}{e}{fc.end}')
        sys.exit()


except KeyboardInterrupt:
        print('Abort')
        sys.exit()