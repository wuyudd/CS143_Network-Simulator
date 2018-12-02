import collections
import heapq
import global_var
import global_consts
import router
import host
from simulator import *
from event import *
import event_type


class Link(object):
    def __init__(self, id, link_rate, link_delay, buffer_size, start, end):
        # all time is in second
        # all link rate is in Mbps
        # all data_size is in byte
        self.id = id
        self.cur_size = 0.0
        self.max_size = buffer_size*1024

        self.buffer = collections.deque()
        self.on_the_link = collections.deque()

        self.link_rate = link_rate
        self.link_delay = link_delay

        self.start = start
        self.end = end

        self.plot_link_buffer_time = []
        self.plot_link_buffer = []

        self.plot_link_rate = []
        self.plot_link_rate_size = 0.0
        self.num_lost_pkt = 0.0


    def __lt__(self, other):
        return self.id < other.id

    def add_packet_to_buffer(self, pkt):
        if pkt.type != 'hello' and isinstance(self.start, router.Router):
            self.start.out_pkt_size[self.id] += pkt.size

        if self.cur_size + pkt.size <= self.max_size:
            print('2')
            #if isinstance(self.start, host.Host):
            #    print(str(global_var.timestamp) + ', ' + self.start.id + ' send ' +  pkt.id)
            self.buffer.append(pkt)
            # cur_event is a new event to move packet from buffer to link
            self.cur_size += pkt.size
            expected_waiting_time = self.cur_size*8/(self.link_rate*1024*1024)#self.data_pkt_cnt * 8/(1024*1) + self.ack_pkt_cnt / (2048*1)  # in s
            cur_event = event_type.FetchFromBuffer(self, global_var.timestamp+expected_waiting_time)
            print('+++++++++++++++++++++++++'+ str(global_var.timestamp+expected_waiting_time) + '-------------------------')
            heapq.heappush(global_var.queue, cur_event)
            # plot function
            self.plot_link_buffer_time.append(global_var.timestamp)
            self.plot_link_buffer.append(self.cur_size)
        else:
            self.num_lost_pkt += 1

    def buffer_to_link(self):
        cur_event = event_type.FetchFromLink(self, global_var.timestamp+self.link_delay)
        heapq.heappush(global_var.queue, cur_event)
        pkt = self.buffer.popleft()
        print('1')
        self.cur_size -= pkt.size
        self.on_the_link.append(pkt)
        # plot function
        self.plot_link_buffer_time.append(global_var.timestamp)
        self.plot_link_buffer.append(self.cur_size)

        self.plot_link_rate_size += pkt.size

    def fetch_from_link(self):
        cur_pkt = self.on_the_link.popleft()
        #self.plot_link_rate_size += cur_pkt.size
        self.end.receive_packet(cur_pkt, self)
