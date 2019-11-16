#!/usr/bin/env python3

"""MITM
Para permitir que la máquina atacante redirija las peticiones es necesario ejecutar
echo 1 > /proc/sys/net/ipv4/ip_forward
"""

import scapy.all as scapy

"""
con scapy se apilan capas con '/'
mandando pkg:
    por capa:
        layer3 (scapy se lo hace todo) -> send, sr, sr1, srloop ..
        layer2 (necesita ser alimentado) -> sendP, srP ...
    por tipo:

"""

# las operaciones de arp 1 y 2 son who-has o is_at
"""
    
"""
