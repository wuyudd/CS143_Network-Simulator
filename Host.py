# class Hosts
# variables: ID (unique)
# methods:
#   1. generate packets for link
#   2. receive packets for flow

# need to call variables/functions from class Packet and Links
from Packet import Packet
from Links import Links

class Host(object):
    def __init__(self, identity, connected_link):
        # every host can be linked to only one link
        if len(connected_link) == 1:
            self.id = identity
            self.link = connected_link
        else:
            raise ValueError('Error: Host Connected with more than 1 link!')

    # get the connected link to host
    def get_link(self):
        return self.link

    # interface for link
    # function: send packets to link
    def send_pkt(self, to_send_pkt):

        # call the addPacketToLink() from Links
        link.addPacketToLink(to_send_pkt)

    # interface for flow
    # function: receive "ACK" or "DATA" type packets for flow
    def receive_pkt(self, to_receive_pkt):
        # call the gettype() from Packet
        if to_receive_pkt.gettype() == "ACK" or to_receive_pkt.gettype() == "DATA":
            # flow receive the "ACK" or "DATA" packets (there are only these two types of valid packets)
            pass
        else
            raise ValueError('Error: Undefined packet type!')
