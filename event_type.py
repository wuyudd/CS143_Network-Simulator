"""
event_type.py defines all types of events.
Every event type inherit from Event class in event.py.
Current event types:
    FlowInitialize
    FetchFromBuffer
    FetchFromLink
    CheckLinkRate
    SayHello
    UpdateRoutingInfo
    UpdateRoutingTable
    FastRecordWindowSize
    TimeOut
"""

from simulator import *
from event import *
import global_consts
import global_var
import heapq


# initialize each flow
class FlowInitialize(Event):
    def __init__(self, flow, start_time):
        self.flow = flow
        self.start_time = start_time

    def action(self):
        self.flow.generate_packet()
        self.flow.flow_send_pkt()
        self.flow.set_new_timeout()


# fetch packet from link buffer to link
class FetchFromBuffer(Event):
    def __init__(self, link, start_time):
        self.link = link
        # start_time is the estimated time to fetch packet from buffer to link.
        # the estimated time is based on the current timestamp and the link rate the process the packet.
        self.start_time = start_time

    def action(self):
        self.link.buffer_to_link()


# the end of the link receives the packet from the link
class FetchFromLink(Event):
    def __init__(self, link, start_time):
        self.link = link
        self.start_time = start_time

    def action(self):
        self.link.fetch_from_link()


# check link rate (Mbps) for each link periodically (for plotting)
class CheckLinkRate(Event):
    def __init__(self, links, start_time):
        self.links = links
        self.start_time = start_time

    def action(self):
        for link in self.links.values():
            # Mbps
            link.plot_link_rate.append((link.plot_link_rate_size*8/1024**2) / global_consts.READLINKRATEFREQUENCY)
            link.plot_link_rate_size = 0
        global_var.plot_link_rate_time_axis.append(self.start_time)


# let each router know their neighbours so as to update routing information
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


# update routing information for routers periodically
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


# run dijkstra periodically after collecting routing information
class UpdateRoutingTable(Event):
    def __init__(self, routers, start_time):
        self.routers = routers
        self.start_time = start_time

    def action(self):
        for router in self.routers.values():
            router.dijkstra()
        global_var.updating_flag = False
        global_var.period += 1


# record window size every RTT for FAST-TCP
class FastRecordWindowSize(Event):
    def __init__(self, flow, start_time):
        self.flow = flow
        self.start_time = start_time

    def action(self):
        self.flow.fast_record_window_size()


# process time out
class TimeOut(Event):
    def __init__(self, flow, start_time):
        self.flow = flow
        self.start_time = start_time

    def action(self):
        # host check ACK
        # if time out, retransmit the time-out packet, change the current state and set new time out.
        self.flow.time_out(self.start_time)