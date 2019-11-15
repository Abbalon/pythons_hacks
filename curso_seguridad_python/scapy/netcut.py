#!/usr/bin/env python3
"""NetCut
Capturalemos paquetes  y los transformaremos
"""

# necesitamos instalar netfilterqueue

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # volvemos a sacar la salida
    print(scapy_packet)  # Mostramos la transformación
    print(packet.get_payload())  # Muesta la entrada
    packet.accept()  # Reencviar
    # packet.drop()  # Eliminar


queue = netfilterqueue.NetfilterQueue()
# Capturamos los paquetes en tránsito
# iptables -I FORWARD -j NFQUEUE --queue-num 0
queue.bind(0, process_packet)
queue.run()

# Capturamos los paquetes que salen
# iptables -I OUTPUT -j NFQUEUE --queue-num 0

# Capturamos los paquetes que entran
# iptables -I INPUT -j NFQUEUE --queue-num 0

# Borramos el SNIFFER
# iptables --flush
