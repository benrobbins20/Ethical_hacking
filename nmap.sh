#!/usr/bin/bash
read -p 'Target IP: ' IP
ports=$(nmap -p- --min-rate=1000  -T4 $IP | grep ^[0-9] | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)
echo $ports

