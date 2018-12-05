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
        self.flow_cnt = {}

        # for reno
        self.lost_pkts_num = collections.deque()

    def send_packet(self, to_send_pkt):
        self.outgoing_links.add_packet_to_buffer(to_send_pkt)

    def receive_packet(self, pkt, link):
        # for debug
        #print(str(round(global_var.timestamp, 7)) + ", " + self.id + ' recieve '+ pkt.id)
        curr_flow_id = pkt.id.split("pkt")[0]
        self.flow_cnt[curr_flow_id] = self.flow_cnt.get(curr_flow_id, '0')

        if pkt.type == "data":
            curr_pkt_num = pkt.id.split("pkt")[1]

            if int(curr_pkt_num) == int(self.flow_cnt[curr_flow_id]):
                ack_pkt = Packet(pkt.id + "ack" + str(int(self.flow_cnt[curr_flow_id]) + 1), "data_ack",global_consts.ACKSIZE, pkt.end, pkt.start)
                self.flow_cnt[curr_flow_id] = str(int(curr_pkt_num) + 1)
                self.outgoing_links.add_packet_to_buffer(ack_pkt)

            else:
                if int(curr_pkt_num) > int(self.flow_cnt[curr_flow_id]):
                    for i in range(int(self.flow_cnt[curr_flow_id]), int(curr_pkt_num)):
                        self.lost_pkts_num.append(i)
                    ack_pkt = Packet(pkt.id + "ack" + str(self.lost_pkts_num[0]), "data_ack", global_consts.ACKSIZE, pkt.end, pkt.start)
                    self.flow_cnt[curr_flow_id] = str(int(self.flow_cnt[curr_flow_id]) + 1)
                    self.outgoing_links.add_packet_to_buffer(ack_pkt)

                elif self.lost_pkts_num and int(curr_pkt_num) == self.lost_pkts_num[0]:
                    self.lost_pkts_num.popleft()
                    if self.lost_pkts_num:
                        self.flow_cnt[curr_flow_id] = str(self.lost_pkts_num[0])
                    ack_pkt = Packet(pkt.id + "ack" + str(int(self.flow_cnt[curr_flow_id])), "data_ack",
                                     global_consts.ACKSIZE, pkt.end, pkt.start)
                    self.flow_cnt[curr_flow_id] = str(int(self.flow_cnt[curr_flow_id]) + 1)
                    self.outgoing_links.add_packet_to_buffer(ack_pkt)

        if pkt.type == "data_ack":
            self.flows[curr_flow_id].receive_ack(pkt)

        if pkt.type == "hello":
            self.neighbors[link.start.id] = self.outgoing_links

    def say_hello(self):
        hello_pkt = Packet("HelloFrom"+self.id, "hello", global_consts.ACKSIZE, self, self.outgoing_links.end)
        self.outgoing_links.add_packet_to_buffer(hello_pkt)