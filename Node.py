from Link import Link

class Node(object):
    def __init__(self, id):
        self.incoming_links = []
        self.outgoing_links = []
        self.id = id

    def send(self):

        return

    def recieve(self,pkt,link):
        if link not in self.incoming_links:
            print(link.id+' not in incoming link of '+self.id)
        packet = link.pick_packet_from_link(pkt)
        print('Recieve '+packet.id)
        return
