#! /usr/bin/python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import matplotlib 
matplotlib.use('Agg') 
from scapy.all import *

dst_ip = "172.16.111.135"
src_port = RandShort()
dst_port = 80

tcpstealthscan_pkts = sr1(
    IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags="S"), timeout=10)
if tcpstealthscan_pkts is None:
    print("Filtered")
elif(tcpstealthscan_pkts.haslayer(TCP)):
    if(tcpstealthscan_pkts.getlayer(TCP).flags == 0x12):
        send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port, flags="R"), timeout=10)
        print("Open")
    elif (tcpstealthscan_pkts.getlayer(TCP).flags == 0x14):
        print("Closed")
elif(tcpstealthscan_pkts.haslayer(ICMP)):
    if(int(tcpstealthscan_pkts.getlayer(ICMP).type) == 3 and int(tcpstealthscan_pkts.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]):
        print("Filtered")
