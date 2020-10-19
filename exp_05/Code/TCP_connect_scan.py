#! /usr/bin/python

import matplotlib 
matplotlib.use('Agg')
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.layers.inet import IP,UDP, TCP, ICMP
from scapy.all import sr,sr1,RandShort


dst_ip = "172.16.111.135"
src_port = RandShort()
dst_port=80

tcpconnectscan_pkts = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=10)
if(str(type(tcpconnectscan_pkts))=="<type 'NoneType'>"):
    print("Filtered")
elif(tcpconnectscan_pkts.haslayer(TCP)):
    if(tcpconnectscan_pkts.getlayer(TCP).flags == 0x12):
        send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="AR"),timeout=10)
        print("Open")
    elif (tcpconnectscan_pkts.getlayer(TCP).flags == 0x14):
        print("Closed")
elif(tcpconnectscan_pkts.haslayer(ICMP)):
    if(int(tcpconnectscan_pkts.getlayer(ICMP).type)==3 and int(tcpconnectscan_pkts.getlayer(ICMP).code) in [1,2,3,9,10,13]):
        print(("Filtered"))
