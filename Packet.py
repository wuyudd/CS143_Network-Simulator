class Packet(object):
    def __init__(self, ID, type, size, end1, end2):
        self.ID =ID
        self.type=type
        self.size=size
        self.end1=end1
        self.end2=end2

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



