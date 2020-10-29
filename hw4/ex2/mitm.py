from netfilterqueue import NetfilterQueue
from scapy.all import *
import re

def print_and_accept(pkt):
    print(pkt)
    pkt.accept()

def process_packet(pkt):
    ip = IP(pkt.get_payload())
    # Do some stuff
    pkt.accept()       

nfqueue = NetfilterQueue()
nfqueue.bind(1, process_packet)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()    