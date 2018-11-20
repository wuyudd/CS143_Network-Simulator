from Event import Event


class FlowGeneratePkt(Event):
    def __init__(self, flow, start_time):
        self.flow = flow
        self.start_time = start_time

    def action(self):
        # generate pkt from flow to host

class SendPkt(Event):
    def __init__(self, pkt, link):
        self.pkt = pkt
        self.link = link

    def action(self):
        # send pkt to link_id

class TimeOut(Event):
    def __init__(self, pkt, host):
        self.pkt = pkt
        self.host = host

    def action(self):
        # host check ACK

class UpdateRoutingTable(Event):
    def __init__(self, routers):
        self.routers = routers

    def action(self):
        # udpate routing table info

