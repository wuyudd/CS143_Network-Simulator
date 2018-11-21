class Packet(object):
    def __init__(self, id, type, size, end1, end2):
        self.id = id
        self.type=type
        self.size=size
        self.end1=end1
        self.end2=end2
        self.ack = 0

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

    def get_ack(self):
        return self.ack



