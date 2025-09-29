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

    reports = []
   

    reports.append(f"System Report - {datetime.now()}" )
    reports.append("\n")
    reports.append("="*55)

    # Find Hostname and Domain Name - Section 1
    reports.append("Device Information \n")
    cmd1 = subprocess.run("hostname", capture_output=True, text= True, shell= True)
    hostname = cmd1.stdout.strip()
    cmd2 = subprocess.run("domainname", capture_output=True, text= True, shell= True)
    domainname = cmd2.stdout.strip()
    reports.append(f"Hostname:                    {hostname}")
    reports.append(f"Domain Name:                    {domainname}")

    reports.append("\n")
    #Section 2 - Network Info
    reports.append("Network Information \n")
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
    reports.append(f"IP Address:                      {ip_addr}")
    reports.append(f"Gateway:                         {gateway}")
    reports.append(f"Network Mask:                    {netMask}")
    reports.append(f"DNS1:                            {DNS1}")
    reports.append(f"DNS2:                            {DNS2}")

    reports.append("\n")
    #Section 3 - OS INFO
    reports.append("Operating System Information \n")
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
    reports.append(f"Operating System:                    {os_name}")
    reports.append(f"OS Version:                       {os_v}")
    reports.append(f"Kernel Version:                      {kernel}")

    reports.append("\n")
    # Section 4 - Storage
    reports.append("Storage Information \n")
    cmd8 =  subprocess.run("df -h /", capture_output=True, text= True, shell= True)
    t = cmd8.stdout.strip()
    t2 = t.split("\n")
    t3 = t2[1].split()
    size = t3[1]
    used = t3[2]
    free = t3[3]
    reports.append(f"Drive Total:                    {size}")
    reports.append(f"Drive Used:                     {used}")
    reports.append(f"Drive Free:                     {free}")

    reports.append("\n")
    # Section 5 - Processor Info
    reports.append("Processor Information \n")
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
    reports.append(f"CPU Model:                        {c_name}")
    reports.append(f"Number of Processors:                    {pr}")
    reports.append(f"Number of Cores:                         {num_cores}")

    reports.append("\n")
    # Section 6 - Ram
    reports.append("Memory Information \n")
    cmd_2 = subprocess.run("free | grep 'Mem:'", capture_output=True, text= True, shell= True)
    lines = cmd_2.stdout
    r = lines.split()
    total = r[1]
    fr_space = r[3]
    reports.append(f"Total RAM:                        {total}")
    reports.append(f"Available RAM:                    {fr_space}")
   
    for line in reports:
        print(line)
   
    with open(logfile,"w") as f:
        for line in reports:
            f.write(line + "\n")
   



if __name__ == '__main__':
    main()