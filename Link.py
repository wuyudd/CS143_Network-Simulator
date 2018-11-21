import collections
import heapq
from Simulator import Simulator
from Event import Event
import EventType


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
            cur_event = EventType.FetchFromBuffer(self, Simulator.timestamp+len(self.buffer)*8/(self.link_rate*1024))
            heapq.heappush(Simulator.queue,(Simulator.timestamp, cur_event))

    def buffer_to_link(self):
        cur_event = EventType.FetchFromLink(self, Simulator.timestamp+self.link_delay)
        heapq.heappush(Simulator.queue, (Simulator.timestamp, cur_event))
        self.on_the_link.append(self.buffer.popleft())

    def fetch_from_link(self):
        self.link.end.recieve_packet(self.on_the_link.popleft())
