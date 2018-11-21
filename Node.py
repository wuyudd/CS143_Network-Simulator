from Link import Link

class Node(object):
    def __init__(self, id):
        self.incoming_links = []
        self.outgoing_links = []
        self.id = id

    def send(self):

        return

    def recieve_packet(self, pkt):
        print('Recieve '+pkt.id)
        return
