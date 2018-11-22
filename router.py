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
        self.routing_pkt_pool = {}
        self.routing_map = {}

    def receive_packet(self, pkt):
        type = pkt.type
        if type == "data" or type == "data_ack":
            self.send(pkt)
        elif type == "routing": # bypass routing information
            if global_var.updating_flag == True:
                s = pkt.id.split("_")
                if(int(s[1]) == global_var.period):
                    if s[2] not in self.routing_pkt_pool:
                        self.routing_pkt_pool.add(s[2])
                        for key in pkt.info.keys():
                            self.routing_map[key] = pkt.info[key]

                        for curr_link in self.outgoing_links.values():
                            if(curr_link.end != pkt.start):
                                curr_pkt = Routing_Packet(pkt.id, "routing", global_consts.PACKETSIZE, self, curr_link.end, pkt.info)
                                curr_link.add_packet_to_buffer(curr_pkt)
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

    def broadcast_routing_pkt(self):
        weight = 1
        period = 1
        for curr_link in self.outgoing_links.values():
            info = {(self.id, curr_link.end.id): weight}

        for curr_link in self.outgoing_links.values():
            id = "P_" + str(period)+ "_" + self.id
            routing_pkt = Routing_Packet(id, "routing", global_consts.PACKETSIZE, self, curr_link.end, info)
            curr_link.add_packet_to_buffer(routing_pkt)


