#!/usr/bin/env python3
import subprocess
import optparse
import re
import os
import sys

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

def get_current_mac(interface):
    try:
        output = subprocess.check_output(["ifconfig", interface]).decode()
        mac_address_search = re.search(r"ether (\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", output)
        if mac_address_search:
            return mac_address_search.group(1)
        else:
            return None
    except subprocess.CalledProcessError:
        return None

def check_root():
    if os.geteuid() != 0:
        sys.exit("[-] Please run as root (use sudo).")

if __name__ == "__main__":
    check_root()
    options = get_arguments()
    current_mac = get_current_mac(options.interface)
    if current_mac:
        print(f"[+] Current MAC = {current_mac}")
    else:
        print("[-] Could not read MAC address.")
    
    change_mac(options.interface, options.new_mac)
    
    updated_mac = get_current_mac(options.interface)
    if updated_mac == options.new_mac:
        print(f"[+] MAC address was successfully changed to {updated_mac}")
    else:
        print("[-] MAC address did not change.")
