#!/usr/bin/env python3
"""
Stript que detecta si nos están redirigiendo
"""

import scapy.all as scapy


def scan(ip="10.0.2.1"):
    arp = scapy.ARP(pdst=ip)  # Seteamos el valor
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp
    # Seleccionamos solo el primer elemento de la lista
    net_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    mac_list = []
    for terminal in net_list:
        ip_mac = {"ip": terminal[1].psrc, "mac": terminal[1].hwsrc}
        mac_list.append(ip_mac)
    return mac_list


def sniff(interface="eth0"):
    scapy.sniff(iface=interface, store=False, prn=porcess_sniffed_packet)
    # , filter=["udp","tcp", "ftp", "arp", "port 80"])


def porcess_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = scan(packet[scapy.ARP].psrc)
            real_mac = real_mac[0]["mac"]
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac != response_mac:
                print("We're being attacked!")
        except IndexError:
            pass


sniff()
