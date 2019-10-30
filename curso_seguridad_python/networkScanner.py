#!/usr/bin/env python3

"""Codigo para realizar un network scaner"""
# $ netdiscover -r 10.0.2.1/24
# $ route -n

import scapy.all as scapy
import subprocess
import optparse
import re

parser = optparse.OptionParser()

parser.add_option("-i", "--interface", dest="iface", help="Interface to change the mac address")
parser.add_option("-m", "--mac", dest="mac", help="The new mac")

(opt, args) = parser.parse_args()

iface = opt.iface
mac = opt.mac

def scan(ip):
    print(ip)
    arp = scapy.ARP(pdst=ip)# Seteamos el valor
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp
    print(arp_request_broadcast.summary()) # Imprime un resumen del resultado
    respondido, irrespondido = scapy.srp(arp_request_broadcast, timeout=2)
    print(respondido.summary())


# Buscamos nuestra ip local, y mandamos un mensaje broadcast
# Se puede sustituir por
ifconfig_result = subprocess.check_output(["ifconfig", iface])

# Expresiones regulares
local_ip = re.search(r"inet (\d{1,3}.){3}\d{1,3}", str(ifconfig_result))
ip = re.search(r"(\d{1,3}.){3}\d{1,3}", str(local_ip.group(0)))
scan(ip.group(0) + "/24")
