#!/usr/bin/python3


import subprocess
import optparse
import time
import random
import re
#display ifconfig to get interface options
#print("View ifconfig for possible interfaces")
#subprocess.call(["ifconfig"])
def get_args():

	parser = optparse.OptionParser()
	parser.add_option("-i","--interface", dest="interface",help="Select interface to change its MAC")
	parser.add_option("-m","--mac address", dest="mac",help="Allows yoou to manually enter MAC address. Leave blank to generate random MAC address")
	parser.set_defaults(mac=rand_mac)
	(options,arguments) = parser.parse_args()
	if not options.interface:
		parser.error("Enter interface to change MAC address.")
	if not options.mac:
		print("No MAC entered. Generating random MAC address...")	

	return options

	

#subprocess.call(["ifconfig"])
def random_mac_gen():
	hex_list = ['a','b','c','d','e','f',1,2,3,4,5,6,7,8,9]
	binary_mac = ([f"{random.randint(0, 255):02x}" for x in range(6)])
	binary_mac = ":".join(binary_mac)
	#print(binary_mac)
	return binary_mac







rand_mac = random_mac_gen()	
def mac_changer(inter,address=rand_mac):
	
	while address != mac_returner(inter):

		#(mac_returner(opt.interface))
		#print("test1")
		#print(address)
		#print(rand_mac)
		#print(inter)
		print("Changing {} interface MAC to {}".format(inter,address))
		time.sleep(5)
		subprocess.call(["sudo" ,"ifconfig", inter, "down"])
		subprocess.call(["sudo" ,"ifconfig", inter, "hw", "ether" ,address])
		subprocess.call(["sudo" ,"ifconfig", inter, "up"])
		subprocess.call(["sudo", "ifconfig", inter])
		try:
			subprocess.call(["expressvpn", "status"])
			print("Reconnecting VPN...")
		except FileNotFoundError:
			pass

		if address == mac_returner(inter):
			return "MAC address has been changed to {}".format(address)
		else:
			address = random_mac_gen()



	





def mac_returner(inter):

	pipecmd = "ifconfig " + opt.interface + " | grep ether | awk '{print $2}'"
	ifconfig_out = subprocess.check_output(["ifconfig", opt.interface])
	ifconfig_str = ifconfig_out.decode('utf-8')
	out = subprocess.check_output(pipecmd, shell=True)
	search_results_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_str)
	if search_results_mac:
		print(search_results_mac.group(0))
	else:
		print("Could not retrieve MAC address. Check interface.")
	return search_results_mac.group(0)



opt = get_args()
print(mac_changer(opt.interface,opt.mac))
