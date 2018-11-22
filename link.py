import collections
import heapq
import global_var
from simulator import *
from event import *
import event_type


class Link(object):
    def __init__(self, id, link_rate, link_delay, buffer_size, start, end):
        # all time is in second, all data size is in Mb
        self.id = id
        self.size = buffer_size
        self.buffer = collections.deque()
        self.on_the_link = collections.deque()
        self.link_rate = link_rate
        self.link_delay = link_delay
        self.start = start
        self.end = end

    def add_packet_to_buffer(self, pkt):
        if len(self.buffer) < self.size:
            self.buffer.append(pkt)
            # t = length_of_queue * packet_size/link_rate
            # t is in second
            # cur_event is a new event to move packet from buffer to link
            cur_event = event_type.FetchFromBuffer(self, global_var.timestamp+len(self.buffer)*8/(self.link_rate*1024))
            heapq.heappush(global_var.queue, cur_event)

    def buffer_to_link(self):
        cur_event = event_type.FetchFromLink(self, global_var.timestamp+self.link_delay)
        heapq.heappush(global_var.queue, cur_event)
        self.on_the_link.append(self.buffer.popleft())

    def fetch_from_link(self):
        self.end.receive_packet(self.on_the_link.popleft())
