#! /usr/bin/python3
# Susan Olayemi
# Sunday, September 28th, 2025

import subprocess
import platform
import os
from datetime import datetime

def get_gateway():
    try:
        result = subprocess.run(["ip","route"], capture_output=True, text= True, check= True)
        output = result.stdout.splitlines()
        #gets the result and goes through each line until it gets to the line that starts with default
        for line in output:
            if line.startswith("default"):
                splited = line.split()
                g_num = splited.index("via") + 1
                return splited[g_num]
   
    except Exception as e:
        print(f"Getting gateway error: {e}")

def main():
    subprocess.run("clear")
    hostname = platform.node()
    logfile = os.path.expanduser(f"~/{hostname}_system_report.log")

    with open(logfile,"w") as file:
        def write_print(message=""):
            print(message)
            file.write(message + "\n")

    write_print(f"System Report - {datetime.now()}" )
    write_print("\n")

    # Find Hostname and Domain Name - Section 1
    write_print("Device Information \n")
    cmd1 = subprocess.run("hostname", capture_output=True, text= True, shell= True)
    hostname = cmd1.stdout.strip()
    cmd2 = subprocess.run("domainname", capture_output=True, text= True, shell= True)
    domainname = cmd2.stdout.strip()
    write_print(f"Hostname:                    {hostname}")
    write_print(f"Domain Name:                    {domainname}")

    write_print("\n")
    #Section 2 - Network Info
    write_print("Network Information \n")
    cmd3= subprocess.run(["hostname -I"], capture_output=True, text= True, shell= True)
    ip_addr = cmd3.stdout.strip()
    gateway = get_gateway()
    cmd4 = subprocess.run("ifconfig | grep 'netmask' | awk '{print $4}'", capture_output=True, text= True, shell= True)
    temp = cmd4.stdout.strip()
    temp2 = temp.split("\n")
    netMask = temp2[0]
    cmd5 = subprocess.run("cat /etc/resolv.conf | grep 'nameserver'| awk '{print $2}'", capture_output=True, text= True, shell= True)
    camp = cmd5.stdout.strip()
    camp2 = camp.split()
    DNS1 = camp2[0]
    DNS2 = camp2[1]
    write_print(f"IP Address:                      {ip_addr}")
    write_print(f"Gateway:                         {gateway}")
    write_print(f"Network Mask:                    {netMask}")
    write_print(f"DNS1:                            {DNS1}")
    write_print(f"DNS2:                            {DNS2}")

    write_print("\n")
    #Section 3 - OS INFO
    write_print("Operating System Information \n")
    cmd6 = subprocess.run("cat /etc/*release", capture_output=True, text= True, shell= True)
    tr = cmd6.stdout.strip()
    #os name
    tr2 = tr.split("\n")
    tri = tr2[6].split("=")
    os_name = tri[1]
    #os version
    v = tr2[4].split("=")
    os_v = v[1]
    #Kernel
    cmd7 =  subprocess.run("hostnamectl | grep 'Kernel'", capture_output=True, text= True, shell= True)
    k = cmd7.stdout.strip()
    k1 = k.split()
    kernel = k1[2]
    write_print(f"Operating System:                    {os_name}")
    write_print(f"OS Version:                       {os_v}")
    write_print(f"Kernel Version:                      {kernel}")

    write_print("\n")
    # Section 4 - Storage
    write_print("Storage Information \n")
    cmd8 =  subprocess.run("df -h /", capture_output=True, text= True, shell= True)
    t = cmd8.stdout.strip()
    t2 = t.split("\n")
    t3 = t2[1].split()
    size = t3[1]
    used = t3[2]
    free = t3[3]
    write_print(f"Drive Total:                    {size}")
    write_print(f"Drive Used:                     {used}")
    write_print(f"Drive Free:                     {free}")

    write_print("\n")
    # Section 5 - Processor Info
    write_print("Processor Information \n")
    cmd8 = subprocess.run("lscpu | grep 'Model name'", capture_output=True, text= True, shell= True)
    p = cmd8.stdout.strip()
    p2 = p.split(":")
    c_name = p2[1]
    cmd9 = subprocess.run("lscpu | grep 'Socket(s):' | awk '{print $2}'", capture_output=True, text= True, shell= True)
    pr = cmd9.stdout.strip()
    cmd0 = subprocess.run("lscpu | grep 'Socket(s):' | awk '{print $2}'", capture_output=True, text= True, shell= True)
    cmd_1 = subprocess.run("lscpu | grep '^Core(s) per socket:' | awk '{print $4}'", capture_output=True, text= True, shell= True)
    c1 = cmd0.stdout.strip()
    c2 = cmd_1.stdout.strip()
    num_cores = int(c1) * int(c2)
    write_print(f"CPU Model:                        {c_name}")
    write_print(f"Number of Processors:                    {pr}")
    write_print(f"Number of Cores:                         {num_cores}")

    write_print("\n")
    # Section 6 - Ram
    write_print("Memory Information \n")
    cmd_2 = subprocess.run("free | grep 'Mem:'", capture_output=True, text= True, shell= True)
    lines = cmd_2.stdout
    r = lines.split()
    total = r[1]
    fr_space = r[3]
    write_print(f"Total RAM:                        {total}")
    write_print(f"Available RAM:                    {fr_space}")
   



if __name__ == '__main__':
    main()