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
    def __init__(self, link, pkt, start_time):
        self.link = link
        self.pkt = pkt
        self.start_time = start_time

    def action(self):
        self.link.transmit(self.pkt)

class FetchFromLink(Event):
    def __init__(self, reciever, link ,pkt , start_time):
        self.link = link
        self.reciever = reciever
        self.pkt = pkt
        self.start_time = start_time

    def action(self):
        self.reciever.recieve(self.pkt,self.link)


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

