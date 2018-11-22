from link import *
import global_var

class Node(object):
    def __init__(self, id):
        self.id = id

    #def send_packet(self, pkt):
    #    self.outgoing_links[0].add_packet_to_buffer(pkt)
    #   return

#    def recieve_packet(self, pkt):
#        print('Recieve '+pkt.id)
#        return
