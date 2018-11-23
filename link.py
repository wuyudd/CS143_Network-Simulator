import collections
import heapq
import global_var
import global_consts
import router
from simulator import *
from event import *
import event_type


class Link(object):
    def __init__(self, id, link_rate, link_delay, buffer_size, start, end):
        # all time is in second, link rate is in Mbps
        self.id = id
        self.size = buffer_size
        self.buffer = collections.deque()
        self.on_the_link = collections.deque()
        self.link_rate = link_rate
        self.link_delay = link_delay
        self.start = start
        self.end = end
        self.plot_link_buffer_time = []
        self.plot_link_buffer = []
        self.ack_pkt_cnt = 0
        self.data_pkt_cnt = 0

    def __lt__(self, other):
        return self.id < other.id

    def add_packet_to_buffer(self, pkt):
        if pkt.type != 'hello' and isinstance(self.start, router.Router):
            self.start.out_pkt_size[self.id] += pkt.size
        if len(self.buffer) < self.size:
            self.buffer.append(pkt)
            # plot function
            self.plot_link_buffer_time.append(global_var.timestamp)
            self.plot_link_buffer.append(len(self.buffer))
            # t = length_of_queue * packet_size/link_rate
            # t is in second
            # cur_event is a new event to move packet from buffer to link
            expected_waiting_time = self.data_pkt_cnt * 8/1024 + self.ack_pkt_cnt /2048  # in s
            cur_event = event_type.FetchFromBuffer(self, global_var.timestamp+expected_waiting_time)
            heapq.heappush(global_var.queue, cur_event)
            # data/routing is 1024 KB
            if pkt.size == global_consts.PACKETSIZE:
                self.data_pkt_cnt += 1
            # data_ack/hello is 64 KB
            elif pkt.size == global_consts.ACKSIZE:
                self.ack_pkt_cnt += 1

    def buffer_to_link(self):
        cur_event = event_type.FetchFromLink(self, global_var.timestamp+self.link_delay)
        heapq.heappush(global_var.queue, cur_event)
        pkt = self.buffer.popleft()
        self.on_the_link.append(pkt)

        # plot function
        self.plot_link_buffer_time.append(global_var.timestamp)
        self.plot_link_buffer.append(len(self.buffer))

        # data/routing is 1024 KB
        if pkt.size == global_consts.PACKETSIZE:
            self.data_pkt_cnt -= 1
        # data_ack/hello is 64 KB
        elif pkt.size == global_consts.ACKSIZE:
            self.ack_pkt_cnt -= 1

    def fetch_from_link(self):
        self.end.receive_packet(self.on_the_link.popleft(), self)
