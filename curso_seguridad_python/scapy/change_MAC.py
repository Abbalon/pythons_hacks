#!/usr/bin/env python3

import subprocess
import optparse

parser = optparse.OptionParser()

parser.add_option("-i", "--interface", dest="iface", help="Interface to change the mac address")
parser.add_option("-m", "--mac", dest="mac", help="The new mac")

(opt, args) = parser.parse_args()

iface = opt.iface
mac = opt.mac

print("Probamos con un ls -la")
command = "ls -la"
subprocess.call(command, shell = True)

print("Apagamos la inteface que vamos a cambiar su MAC")
command = ["ifconfig",iface, "down"]
subprocess.call([command[0], command[1], command[2]], shell = True)

print("Seteamos la nueva MAC")
command = ["ifconfig",iface, "hw", "ether", mac]
subprocess.call([command[0], command[1], command[2], command[3], command[4], command[5]], shell = True)

print("Volvemos a levantar la interface")
command = ["ifconfig",iface, "up"]
subprocess.call([command[0], command[1], command[2]], shell = True)

print("Listamos el resultad0")
print(subprocess.call(["ifconfig",iface], shell = True))

# Se puede sustituir por
ifconfig_result = subproces.check_output(["ifconfig", iface])

# Expresiones regulares
import re
re.search(r"\s(\w{2}:){5}\w{2}\s", ifconfig_result)
