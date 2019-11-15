#!/usr/bin/env python3
"""
Stript que detecta si nos están redirigiendo
"""

import scapy.all as scapy


def sniff(interface="eth0"):
    scapy.sniff(iface=interface, store=False, prn=porcess_sniffed_packet)
    # , filter=["udp","tcp", "ftp", "arp", "port 80"])


def porcess_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        print(packet.show())


sniff()
