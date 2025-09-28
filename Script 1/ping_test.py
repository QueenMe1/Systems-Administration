#! /usr/bin/python3
# Susan Olayemi
# Wednesday, September 10th, 2025

import subprocess

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

#pings the gateway
def local_connT(gateway):
    try:
        result = subprocess.run(["ping","-c","4",gateway], capture_output=True, text= True, check= True)
        if result.returncode == 0:
            print("LOCAL CONNECTION TEST WORKED!! Ping is successful")
        else: 
            print("request timed out or failed")
    except Exception as e:
        print(f"Gateway cannot be pinged: {e}")

#pings the dns remote ip
def remote_connT():
    try:
        result = subprocess.run(["ping","-c","4","129.21.3.17"], capture_output=True, text= True, check= True)
        if result.returncode == 0:
            print("REMOTE CONNECTION TEST WORKED!! Ping is successful")
        else:
            print("request timed out")
    except Exception as e:
       print(f"remote ip cannot be pinged: {e}")

   #ping google.com and send print if it's successful or not    
def dns_test():
    try:
        result = subprocess.run(["ping","-c","4","www.google.com"], capture_output=True, text= True, check= True)
        if result.returncode == 0:
            print("DNS TEST PASSED!!! Ping is successful")
        else:
            print("request timed out or failed")
    except Exception as e:
       print(f"DNS test did not go through: {e}")

def main():
    while True:
        # assign numbers to each choices
        user_in = input("Enter the number corresponding to you choice:\n"
                        "1. Display the default gateway\n"
                        "2. Test Local Connectivity\n"
                        "3. Test Remote Connectivity\n"
                        "4. Test DNS Resolution\n"
                        "5. Exit/Quit the script\n")
        
        # correspond each number to the functions.
        if user_in == "1":
            print("Your Gateway is " + get_gateway())
        elif(user_in == "2"):
            gt = get_gateway()
            if gt:
                local_connT(gt)
        elif(user_in == "3"):
            remote_connT()
        elif(user_in == "4"):
            dns_test()
        elif(user_in == "5"):
            print("Bye!!")
            break


if __name__ == '__main__':
    main()
    