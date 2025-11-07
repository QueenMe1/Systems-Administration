from pathlib import Path
import re
from geoip import geolite2 
import subprocess

pattern = re.compile(r"Failed Password.*from (\d+\.\d+\.\d+\.\d+)")

def get_home():
    # returns the user's current home directory.
    return Path.home()

def get_login_list():
    ip_add = []
    home = get_home()
    file_path = home / "syslog.log"
    with open(file_path,"r") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                ip_add.append(match.group(1))
    return ip_add

def make_dict():
    addr = get_login_list()
    count_dict = {}
    for ip in addr:
        if ip in count_dict:
            count_dict[ip] += 1
        else:
            count_dict[ip] = 1
    return count_dict

