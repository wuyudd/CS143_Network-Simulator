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
            
    def dijkstra(self):
        counter = 0
        queue = []  # save links by comparing weight, (weight, outgoing_link)
        curr_router = self
        curr_router_link_list = {curr_router.id: []}  # the shortest path from router to curr_router

        # get router and host in the self.routing_map
        router_set = set()
        host_set = set()
        for ele in self.routing_map:
            if ele[0][0].startswith('R'):
                router_set.add(ele[0][0])
            else:
                host_set.add(ele[0][0])
        num_of_hosts = len(host_set) # number of hosts

        while counter < num_of_hosts:
            while isinstance(curr_router, Host):
                # at this time, curr_router is a host instance
                if counter < num_of_hosts:
                    self.routing_table[curr_router.id] = curr_router_link_list[0]  # only need the link from router
                    curr_router = queue.pop()[1].end
                    counter += 1
                else:
                    break
            curr_router_outgoing_links = curr_router.outgoing_links
            for curr_router_outgoing_link in curr_router_outgoing_links:
                curr_router_end = curr_router_outgoing_link.end
                if (self.id, curr_router_end.id) in curr_router.routing_map:
                    curr_router_outgoing_link_weight = curr_router.routing_map[
                        (self.id, curr_router_end.id)]  # get weight from routing_map of curr_router
                    heapq.heappush(queue, (curr_router_outgoing_link_weight, curr_router_outgoing_link))

            curr_min_link = heapq.heappop(queue)[1]
            curr_router_link_list[curr_router.end.id] = curr_router_link_list[curr_router.id].append(curr_min_link)
            curr_router = curr_min_link.end


