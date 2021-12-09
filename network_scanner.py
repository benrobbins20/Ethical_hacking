#!usr/bin/python3

import scapy.all as sc
import subprocess
import re
import argparse

def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--interface',dest='inter',help='Enter interface')
    parser.add_argument("-r","--range",dest="ip_range",help="Enter an IP range to scan")
    parser.set_defaults(inter='eth0')
    options = parser.parse_args()
    return options
opt = get_args()

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
print("Kali MAC Adddress: ",mr)

def scan(address):
    #print(sc.get_if_list())
    request = sc.ARP(pdst = address)
    print(request.summary())
    #print(sc.ls(request))
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast.src = mr   
    request_broadcast = broadcast/request    
    answered_list= sc.srp(request_broadcast,timeout = 1,verbose=False)[0]
    client_list = []
    for elem in answered_list:
        client_dict = {"ip":elem[1].psrc,"mac":elem[1].hwsrc}
        client_list.append(client_dict)
    return client_list
scan_results = scan(opt.ip_range)

def scan_out(results_list):    
    for elem in results_list:
        print("-"*50)
        print(elem)
        print("-"*50)
        print("\n")
    return "Scan Finished"     
print(scan_out(scan_results))