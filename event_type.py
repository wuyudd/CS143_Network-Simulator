import global_var
from event import *
from router import *
from simulator import *
import heapq


class FlowInitialize(Event):
    def __init__(self, flow, start_time):
        self.flow = flow;
        self.start_time = start_time

    def action(self):
        self.flow.generate_packet()
        self.flow.add_event()


class SendFromFlow(Event):
    def __init__(self, flow, pkt, start_time):
        self.flow = flow
        self.pkt = pkt
        self.start_time = start_time

    def action(self):
        #prefix = 'pkt'
        #packet = self.flow.pkt_pool[prefix + str(self.index)]
        self.flow.send_packet(self.pkt)


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
    def __init__(self, pkt, flow, start_time):
        self.pkt = pkt
        self.flow = flow
        self.start_time = start_time

    def action(self):
        # host check ACK
        # if TimeOut, change window size and send again
        #global_var.queue.append(SendPkt())
        # if not Timeout, end
        self.flow.time_out(self.pkt)


class UpdateRoutingInfo(Event):
    def __init__(self, routers, start_time):
        self.routers = routers
        self.start_time = start_time

    def action(self):
        global_var.updating_flag = True
        for router in self.routers.values():
            router.broadcast_routing_pkt()

        event = UpdateRoutingTable(self.routers, self.start_time + global_consts.UPDATEDURATION)
        heapq.heappush(global_var.queue, event)


class UpdateRoutingTable(Event):
    def __init__(self, routers, start_time):
        self.routers = routers
        self.start_time = start_time

    def action(self):
        for router in self.routers.values():
            router.dijkstra()

            # dijkstra
        global_var.updating_flag = False
        global_var.period += 1

class CheckLinkRate(Event):
    def __init__(self, links, start_time):
        self.links = links
        self.start_time = start_time

    def action(self):
        for link in self.links.values():
            link.plot_link_rate.append((link.plot_link_rate_size*8/1024**2) / global_consts.READLINKRATEFREQUENCY)
            link.plot_link_rate_size = 0


class SayHello(Event):
    def __init__(self, routers, hosts, start_time):
        self.routers = routers
        self.hosts = hosts
        self.start_time = start_time

    def action(self):
        for router in self.routers.values():
            router.say_hello()

        for host in self.hosts.values():
            host.say_hello()

