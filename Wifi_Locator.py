from prettytable import PrettyTable
import operator
import subprocess
import os
import math
import re
import schedule
import time


def sniffer():
    # iwlist command to scan all the Access Points
    proc = subprocess.Popen('iwlist wlan0 scan | grep -oE "(ESSID:|Address:|Channel:|Quality=).*" 2>/dev/null',
                            shell=True, stdout=subprocess.PIPE, )
    stdout_str = proc.communicate()[0]
    stdout_list = stdout_str.split('\n')

    # Declaring Lists
    network_name = []
    mac_address = []
    channel = []
    signal = []
    decibel = []
    distance = []
    frequency = []

    # Reading all the Lines
    for line in stdout_list:
        line = line.strip()
        # Regex to Match ESSID Value
        match = re.search('ESSID:"(\S+)"', str(line))
        if match:
            network_name.append(match.group(1))
        # Regex to Match Channel Value
        match = re.search('Channel:(\S*)', str(line))
        if match:
            channel.append(match.group(1))
            # Calculating Frequency
            frequency.append(int(match.group(1)) * 5 + 2407)
        # Regex to Match Address Value
        match = re.search('Address:\s(\S+)', str(line))
        if match:
            mac_address.append(match.group(1))
        # Regex to Match Signal Value
        match = re.search('Signal level=(\S+)', str(line))
        if match:
            signal.append(match.group(1))
            # Sign Correctness
            decibel.append(abs(int(match.group(1))))
    i = 0
    x = PrettyTable()
    x.field_names = ["ESSID", "MAC Address", "Channel", "Signal", "Distance", "Frequency", "Decibel"]
    os.system("clear")
    while i < len(network_name):
        # Free Space Path Loss (FSPL)
        distance = 10 ** ((27.55 - (20 * math.log10(int(frequency[i]))) + int(decibel[i])) / 20)
        # Adding a Row to Pretty Table
        x.add_row([network_name[i], mac_address[i], channel[i], int(signal[i]), str(float(distance)) + " mtr",
                   int(frequency[i]), int(decibel[i])])
        i = i + 1
    print(x.get_string(sort_key=operator.itemgetter(4, 0), sortby="Signal", reversesort=True))
    i = 0


# Main Thread Starts
schedule.every(5).seconds.do(sniffer)
while 1:
    schedule.run_pending()
    time.sleep(1)
