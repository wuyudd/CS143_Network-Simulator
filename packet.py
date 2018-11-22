class Packet(object):
    def __init__(self, id, type, size, start, end):
        self.id = id
        self.type = type
        self.size = size
        self.start = start
        self.end = end
        self.ack = 0

    def getID(self):
        return self.id

    def gettype(self):
        return self.type

    def getsize(self):
        return self.size

    def getend1(self):
        return self.start

    def getend2(self):
        return self.end

    def get_ack(self):
        return self.ack

    def set_ack(self, flag):
        self.ack = flag

class Routing_Packet(Packet):
    def __init__(self, id, type, size, start, end, info):
        super().__init__(id, type, size, start, end)
        self.info = info



