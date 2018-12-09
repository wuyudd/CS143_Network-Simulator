from node import *
from packet import *
from flow import *
import global_var
import global_consts
import collections


class Host(Node):
    def __init__(self, host_ipaddr):
        super().__init__(host_ipaddr)
        self.flows = {}
        self.incoming_links = None
        self.outgoing_links = None
        self.neighbors = {}
        self.flow_lost_pkt_pointer = {}
        self.send_flag = 0

        # for reno
        self.recieved_pkts_data = []

    def send_packet(self, to_send_pkt):
        flow_id = to_send_pkt.id.split('pkt')[0]
        print(flow_id + ':' + ' send ' + to_send_pkt.id)
        self.outgoing_links.add_packet_to_buffer(to_send_pkt)

    def receive_packet(self, pkt, link):
        if pkt.type == "data":
            # if pkt.id == "F1pkt7900" and self.send_flag == 0:
            #     self.send_flag = 1
            # elif pkt.id != "F1pkt7900" or self.send_flag == 1:

            flow_id = pkt.id.split('pkt')[0]
            #print(flow_id + ':' + 'recieve ' + pkt.id)
            self.flow_lost_pkt_pointer[flow_id] = self.flow_lost_pkt_pointer.get(flow_id, -1)
            pkt_ind = int(pkt.id.split('pkt')[1])
            if pkt_ind < len(self.recieved_pkts_data):
                self.recieved_pkts_data[pkt_ind] = 1
            else:
                i = len(self.recieved_pkts_data)
                while i < pkt_ind:
                    self.recieved_pkts_data.append(0)
                    i += 1
                self.recieved_pkts_data.append(1)
            i = self.flow_lost_pkt_pointer[flow_id]
            while i < len(self.recieved_pkts_data) and self.recieved_pkts_data[i] != 0:
                i += 1
            self.flow_lost_pkt_pointer[flow_id] = i
            return_pkt = Packet(pkt.id + "ack" + str(i), "data_ack",
                                     global_consts.ACKSIZE, pkt.end, pkt.start)
            self.outgoing_links.add_packet_to_buffer(return_pkt)


        if pkt.type == "data_ack":
            curr_flow_id = pkt.id.split("pkt")[0]
            self.flows[curr_flow_id].receive_ack(pkt)

        if pkt.type == "hello":
            self.neighbors[link.start.id] = self.outgoing_links

    def say_hello(self):
        hello_pkt = Packet("HelloFrom"+self.id, "hello", global_consts.ACKSIZE, self, self.outgoing_links.end)
        self.outgoing_links.add_packet_to_buffer(hello_pkt)
