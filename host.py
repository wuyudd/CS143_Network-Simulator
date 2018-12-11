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
        self.neighbors = {}  # key is the neighbor node, value is the outgoing_links
        self.flow_lost_pkt_pointer = {} # key is the corresponding flow, value is the first 0's position(this position's pkt has not been acknowleged) in the recieved_pkts_data list
        self.send_flag = 0

        # for reno
        self.recieved_pkts_data = []
        # a list to record whether a pck is received, 0: not received, 1: received

    def send_packet(self, to_send_pkt):
        flow_id = to_send_pkt.id.split('pkt')[0]
        print(flow_id + ':' + ' send ' + to_send_pkt.id)
        self.outgoing_links.add_packet_to_buffer(to_send_pkt)

    def receive_packet(self, pkt, link):
        if pkt.type == "data":
            flow_id = pkt.id.split('pkt')[0]
            self.flow_lost_pkt_pointer[flow_id] = self.flow_lost_pkt_pointer.get(flow_id, -1)
            pkt_ind = int(pkt.id.split('pkt')[1])

            # this pkt has already been recorded in the recieved_pkts_data list, update it's state to be received(value to be 1)
            if pkt_ind < len(self.recieved_pkts_data):
                self.recieved_pkts_data[pkt_ind] = 1
            else:
                i = len(self.recieved_pkts_data)
                #set the state of the pkts between the last one in recieved_pkts_data list and the one we received to be unreceived(value to be 0)
                while i < pkt_ind:
                    self.recieved_pkts_data.append(0)
                    i += 1
                self.recieved_pkts_data.append(1)
            i = self.flow_lost_pkt_pointer[flow_id]
            # update the pointer, point to the pkt to be acknowledged(first 0 in the list)
            while i < len(self.recieved_pkts_data) and self.recieved_pkts_data[i] != 0:
                i += 1
            self.flow_lost_pkt_pointer[flow_id] = i
            return_pkt = Packet(pkt.id + "ack" + str(i), "data_ack",
                                     global_consts.ACKSIZE, pkt.end, pkt.start)
            return_pkt.sending_time = pkt.sending_time
            self.outgoing_links.add_packet_to_buffer(return_pkt)

        # let the corresponding flow to receive data_ack
        if pkt.type == "data_ack":
            curr_flow_id = pkt.id.split("pkt")[0]
            self.flows[curr_flow_id].receive_ack(pkt)

        # construct the host's neighbor, key is the end node's id, value is the link
        if pkt.type == "hello":
            self.neighbors[link.start.id] = self.outgoing_links

        # send hello packet to construct graph
    def say_hello(self):
        hello_pkt = Packet("HelloFrom"+self.id, "hello", global_consts.ACKSIZE, self, self.outgoing_links.end)
        self.outgoing_links.add_packet_to_buffer(hello_pkt)
