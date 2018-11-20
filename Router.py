import collections
import Link
import Packet
from Node import Node

class Router(Node):
    def __init__(self, router_id):
        super().__init__(router_id)
        self.routing_table = {}

    def send(self, packet):
        pass
        #dest = packet.getPacketDestination()
        #link = self.routing_table[dest]
        #link.addPacketToLink(packet)

    def receive(self, packet):
        pass




