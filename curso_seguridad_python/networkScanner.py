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
    respondido = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0] # Seleccionamos solo el primer elemento de la lista

    print("IP\t\t\tMAC")
    print("_________________________________________")
    for response in respondido:
        print(response[1].psrc + "\t\t" + response[1].hwsrc)


# Buscamos nuestra ip local, y mandamos un mensaje broadcast
# Se puede sustituir por
if iface is None:
    iface = "enx34298f9221b9"

ifconfig_result = subprocess.check_output(["ifconfig", iface])

# Expresiones regulares
local_ip = re.search(r"inet (\d{1,3}.){3}\d{1,3}", str(ifconfig_result))
ip = re.search(r"(\d{1,3}.){3}\d{1,3}", str(local_ip.group(0)))
scan(ip.group(0) + "/24")
