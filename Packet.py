class Packet(object):
    def __init__(self, ID, type, size, end1, end2,pos):
        self.ID =ID
        self.pos=pos # in pktpool, the key correspond to this packet, the same in packet and its ack, use the pos in ack to find origin pck
        self.type=type
        self.size=size
        self.end1=end1
        self.end2=end2
        self.ack=0

    def getID(self):
        return self.ID

    def gettype(self):
        return self.type

    def getsize(self):
        return self.size

    def getend1(self):
        return self.end1

    def getend2(self):
        return self.end2

    def getack(self):
        return self.ack

    def set_ack(self,ack):
        self.ack=ack



