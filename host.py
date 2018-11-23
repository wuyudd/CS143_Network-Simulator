from node import *
from packet import *
from flow import *
import global_var
import global_consts


class Host(Node):
    def __init__(self, host_ipaddr):
        super().__init__(host_ipaddr)
        self.flows = {}
        self.incoming_links = None
        self.outgoing_links = None
        self.neightbors = {}

    def send_packet(self, to_send_pkt):
        self.outgoing_links.add_packet_to_buffer(to_send_pkt)

    def receive_packet(self, pkt, link):
        # for debug
        print(str(round(global_var.timestamp, 7)) + ", " + self.id + ' recieve '+ pkt.id)
        if pkt.type == "data":
            ack_pkt = Packet(pkt.id + "ack", "data_ack", global_consts.ACKSIZE, self, pkt.start)
            self.outgoing_links.add_packet_to_buffer(ack_pkt)
        if pkt.type == "data_ack":
            curr_flow_id = pkt.id.split("pkt")[0]
            self.flows[curr_flow_id].receive_ack(pkt)
        if type == "hello":
            self.neighbors[link.start.id] = self.outgoing_links


    def say_hello(self):
        hello_pkt = Packet("HelloFrom"+self.id, "hello", global_consts.PACKETSIZE, self, self.outgoing_links.end)
        self.outgoing_links.add_packet_to_buffer(hello_pkt)