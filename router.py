import collections
import global_var
from link import *
from packet import *
from node import *


class Router(Node):
    def __init__(self, router_id):
        super().__init__(router_id)
        self.incoming_links = {}
        self.outgoing_links = {}
        self.routing_table = {}

    def receive_packet(self, pkt):
        type = pkt.type
        if type == "data" or type == "data_ack":
            self.send(pkt)
        #elif type == "routing":

        #elif type == "routing_ack":

    def send(self, pkt):
        type = pkt.type
        if type == "data" or type == "data_ack":
            end = pkt.end
            link = self.routing_table[end.id]
            link.add_packet_to_buffer(pkt)

        #elif type == "routing":


        #elif type == "routing_ack":
        #    self.update_routing_table(pkt)

    def init_routing_table(self):
        pass

    def update_routing_table(self, pkt):
        pass




