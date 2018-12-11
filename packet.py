class Packet(object):
    def __init__(self, id, type, size, start, end):
        self.id = id
        self.type = type
        # three types of packet: data, data_ack, hello

        self.size = size
        self.start = start #host
        self.end = end #host
        self.ack = 0
        self.sending_time = 0.0
        # data_ack's sending time is the sending time of it's corresponding data packet


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
