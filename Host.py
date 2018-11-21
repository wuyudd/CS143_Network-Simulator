from Node import Node


class Host(Node):
    def __init__(self, host_ipaddr):
        super().__init__(host_ipaddr)
        #super().__init__(host_ipaddr, connected_link)

    #def send_packet(self, to_send_pkt):
        #self.outgoing_links[0].add_packet_to_buffer(to_send_pkt)

    #def receive_packet(self, pkt):
        #for debug
        #print('Recieve '+ pkt.id)
        #self.incoming_links[0].pick_packet_from_link()
