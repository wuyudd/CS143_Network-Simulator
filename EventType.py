from Event import Event
from Simulator import Simulator

class FlowGeneratePkt(Event):
    def __init__(self, flow, start_time):
        self.flow = flow
        self.start_time = start_time

    def action(self):
        # generate pkt from flow to host
        Simulator.queue.append(SendPkt())

class SendPkt(Event):
    def __init__(self,src , pkt, link, start_time):
        self.src = src
        self.pkt = pkt
        self.link = link
        self.start_time = start_time

    def action(self):
        # send pkt to link_id

        Simulator.queue.append(TimeOut())

class FetchFromBuffer(Event):
    def __init__(self, link, start_time):
        self.link = link
        self.start_time = start_time

    def action(self):
        self.link.buffer_to_link()

class FetchFromLink(Event):
    def __init__(self, link, start_time):
        self.link = link
        self.start_time = start_time

    def action(self):
        self.link.fetch_from_link()

class TimeOut(Event):
    def __init__(self, pkt, host, start_time):
        self.pkt = pkt
        self.host = host
        self.start_time = start_time

    def action(self):
        # host check ACK

        # if TimeOut, change window size and send again
        Simulator.queue.append(SendPkt())
        # if not Timeout, end


class UpdateRoutingTable(Event):
    def __init__(self, routers, start_time):
        self.routers = routers
        self.start_time = start_time

    def action(self):
        # udpate routing table info

