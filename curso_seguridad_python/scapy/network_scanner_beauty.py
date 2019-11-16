#!/usr/bin/env python3

"""Código para la tarea 1"""

import scapy.all as scapy
import subprocess
import re
import argparse

def catch_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Chose the target")
    parser.add_argument("-i", "--interface", dest="iface", help="Interface to change the mac address")
    parser.add_argument("-m", "--mac", dest="mac", help="The new mac")
    args = parser.parse_args()

    if args.target is None:
        args.target = get_own_ip()

    return args

def get_own_ip(iface="eth0"):
    """
    Devuelve la ip del sistema en la interface indicada o la interface <i>eth0</i> por defecto
    """
    ifconfig_result = subprocess.check_output(["ifconfig", iface])
    local_ip = re.search(r"inet (\d{1,3}.){3}\d{1,3}", str(ifconfig_result))
    return re.search(r"(\d{1,3}.){3}\d{1,3}", str(local_ip.group(0))).group(0)


def scan(ip="10.0.2.1/24"):
    arp = scapy.ARP(pdst=ip)# Seteamos el valor
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp
    net_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0] # Seleccionamos solo el primer elemento de la lista

    mac_list = []
    for terminal in net_list:
        ip_mac = {"ip": terminal[1].psrc, "mac": terminal[1].hwsrc}
        mac_list.append(ip_mac)

    return mac_list

def show(listado):
    print("IP\t\t\tMAC")
    print("_________________________________________")
    for response in listado:
        print(response["ip"] + "\t\t" + response["mac"])

args = catch_arguments()
# show(scan(args.target + "/24"))
