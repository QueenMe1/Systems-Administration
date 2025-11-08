#! /usr/bin/python3
# Susan Olayemi
# November 7th, 2025

from pathlib import Path
import re
from geoip import geolite2
from datetime import datetime
import subprocess

pattern = r'\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b'


def get_home():
    # returns the user's current home directory.
    return Path.home()

def get_login_list():
    ip_add = {}
    home = get_home()
    file_path = home / "syslog.log"
    with open(file_path,"r") as file:
        for line in file:
            if "Failed password for" in line:
                address_list= re.search(pattern,line)
                if not address_list:
                    continue
                address = address_list.group(0)
                if address not in ip_add:
                    geo = geolite2.lookup(address)
                    location = geo.country if geo else "Unknown"
                    ip_add[address] = {"Count": 1, "Location": location}
                else:
                    ip_add[address]["Count"] += 1
    return ip_add
   
def make_dict2():
    dict1 = get_login_list()
    dict2 = {ip: info for ip,info in dict1.items() if info['Count'] >= 10}
    return dict2
   
def main():
   subprocess.run("clear")
   main_dict = make_dict2()
   sorted_items = sorted(main_dict.items(), key=lambda kv: kv[1]['Count'], reverse=False)

   print(f"Attacker Report - {datetime.now()}")
   print(f"{'COUNT':}           {'IP_ADDRESS':}             {'LOCATION':}")
   for key,info in sorted_items:
       print(f"{info['Count']}              {key}               {info['Location']}")
   

if __name__ == '__main__':
    main()