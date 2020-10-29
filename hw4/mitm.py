from netfilterqueue import NetfilterQueue

# Using example from https://pypi.org/project/NetfilterQueue/

def print_and_accept(pkt):
    print(pkt)
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()    