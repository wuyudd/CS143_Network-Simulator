import collections
import global_var
import global_consts
from link import *
from packet import *
from node import *
from host import *


class Router(Node):
    def __init__(self, router_id):
        super().__init__(router_id)
        self.incoming_links = {}
        self.outgoing_links = {}
        self.neighbors = {}
        self.routing_table = {}
        self.routing_pkt_pool = set()
        self.routing_map = {}
        self.num_edge_on_map = 0
        self.out_pkt_size = {}

    def receive_packet(self, pkt, link):
        type = pkt.type
        #print(self.id + ':'+ 'Recieve ' + pkt.id + '@ P' + str(global_var.period))
        if type == "data" or type == "data_ack":
            self.send(pkt)
        elif type == "routing": # bypass routing information
            #print(self.id+'recieve'+'XXXXXXXXXXXXXXX')
            if global_var.updating_flag == True:
                s = pkt.id.split("_")
                print(s[1])
                print(global_var.period)
                if(int(s[1]) == global_var.period):
                    if s[2] not in self.routing_pkt_pool:
                        self.routing_pkt_pool.add(s[2])
                        for key in pkt.info.keys():
                            self.routing_map[key] = pkt.info[key]
                        for curr_link in self.outgoing_links.values():
                            if(curr_link.end != pkt.start):
                                curr_pkt = Routing_Packet(pkt.id, "routing", global_consts.PACKETSIZE, self, curr_link.end, pkt.info)
                                curr_link.add_packet_to_buffer(curr_pkt)
            print(self.id + ' '+ str(len(self.routing_map)))
        elif type == "hello":
            if link.id[-1] == '*':
                self.neighbors[link.start.id] = self.outgoing_links[link.id[:len(link.id)-1]]
                self.out_pkt_size[link.id[:len(link.id)-1]] = 0
            else:
                self.neighbors[link.start.id] = self.outgoing_links[link.id + '*']
                self.out_pkt_size[link.id + '*'] = 0

    def send(self, pkt):
        type = pkt.type
        if type == "data" or type == "data_ack":
            link = self.routing_table[pkt.end.id]
            link.add_packet_to_buffer(pkt)

    def broadcast_routing_pkt(self):
        info = {}
        for curr_link in self.outgoing_links.values():
            weight = curr_link.link_delay + global_consts.WEIGHTFACTOR * self.out_pkt_size[curr_link.id]/curr_link.link_rate
            info[(self.id, curr_link.end.id)] = weight
            self.routing_map[(self.id, curr_link.end.id)] = weight

        for curr_link in self.outgoing_links.values():
            id = "ROUTINGINFO@P_" + str(global_var.period)+ "_" + self.id
            routing_pkt = Routing_Packet(id, "routing", global_consts.PACKETSIZE, self, curr_link.end, info)
            curr_link.add_packet_to_buffer(routing_pkt)

        # clear out_pkt_size for all links connected to this router
        for key in self.out_pkt_size.keys():
            self.out_pkt_size[key] = 0
    

    def say_hello(self):
        for curr_link in self.outgoing_links.values():
            hello_pkt = Packet("HelloFrom"+self.id, "hello", global_consts.ACKSIZE, self, curr_link.end)
            curr_link.add_packet_to_buffer(hello_pkt)


    def dijkstra(self):
        if global_var.period == 0:
            self.num_edge_on_map = len(self.routing_map)
        #print('!!!!!!!!!!!!!!'+str(len(self.routing_map)))
        #print(self.num_edge_on_map)
        if len(self.routing_map) != self.num_edge_on_map:
            return
        known_dist = {}
        known_dist[self.id] = 0
        unknow_dist = set()
        for key in self.routing_map.keys():
            if key[0] not in known_dist:
                unknow_dist.add(key[0])
            if key[1] not in known_dist:
                unknow_dist.add(key[1])

        #run dijstra

        parent = {self.id: None}
        children = {}
        cur_node = self.id
        cur_dist = 0
        queue = []
        #print(self.routing_map)

        while unknow_dist:
            # print("================")
            # print(unknow_dist)
            # print(known_dist)
            for s,e in self.routing_map.keys():
                if s == cur_node and e not in known_dist:
                    heapq.heappush(queue, (self.routing_map[(s,e)]+cur_dist,(s,e)))
            cur_path_length, cur_link = heapq.heappop(queue)
            #print(cur_link)
            if cur_link[1] not in known_dist:
                known_dist[cur_link[1]] = cur_path_length
                unknow_dist.remove(cur_link[1])
                parent[cur_link[1]] = cur_link[0]
                children[cur_link[0]] = children.get(cur_link[0], []) + [cur_link[1]]
                cur_node = cur_link[1]
                cur_dist = cur_path_length
            #print(unknow_dist)
            #print(queue)

        routing_info = {}
        #recover the shortest path
        for child in children[self.id]:
            routing_info[child] = self.DFS(child, children)
        for key, value in routing_info.items():
            if len(value) != 0:
                dest_list = value.split(' ')
                for dest in dest_list:
                    self.routing_table[dest] = self.neighbors[key]
        print(self.id + 'routing table: ')
        print(self.routing_table)
        val = self.routing_table.values()
        print(self.routing_table['10.10.10.1'].id)
        print(self.routing_table['10.10.10.2'].id)
        self.routing_map = {}
        self.routing_pkt_pool = set()

    def DFS(self,  cur, children):
        if cur[0].isdigit():
            return cur
        if cur not in children:
            return ''
        s = ''
        for child in children[cur]:
            if s != '':
                s = s+' '+self.DFS(child, children)
            else:
                s += self.DFS(child, children)
        return s








