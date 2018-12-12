"""
link.py maintains the Link class.
Link has the function including add_packet_to_buffer, buffer_to_link, fetch_from_link
so as to transmit the packets from one end of the link to the other.
"""
import collections
import heapq
import global_var
import global_consts
import router
import host
from simulator import *
import event_type


class Link(object):
    def __init__(self, id, link_rate, link_delay, buffer_size, start, end):
        # link delay is in second
        # input link rate is in Mbps
        # input buffer_size is in KByte
        # link id is a string
        self.id = id
        # the current size of buffer is in byte
        self.cur_size = 0.0
        # the maximum size of buffer is in byte
        self.max_size = buffer_size*1024
        # the link_lock is set to True when link is pushing packet from buffer to link
        # the link_lock is set to False when link is idle (not pushing packet from buffer to link)
        self.link_lock = False
        # buffer is a double ended queue to store the packet waiting for sending
        self.buffer = collections.deque()
        # on_the_link is a double ended queue to store the packet on the link (the packet is waiting for propagation delay)
        self.on_the_link = collections.deque()
        # link_rate specifie the link rate for this link
        self.link_rate = link_rate
        # link_delay specifies the propagation delay for this link
        self.link_delay = link_delay
        # start specifies the start node of this link(a host or a router)
        self.start = start
        # start specifies the end node of this link(a host or a router)
        self.end = end

        # for visualization purpose
        #  plot_link_buffer_time specifies the time axis for buffer
        self.plot_link_buffer_time = []
        # plot_link_buffer specifies the buffer size for whole process
        self.plot_link_buffer = []
        # plot_link_rate specifies the link rate for whole process
        self.plot_link_rate = []
        # plot_link_rate_size specify the the size of packets sent in a certain interval
        # reset to 0 when one interval passes
        self.plot_link_rate_size = 0.0
        # used for debug, num_lost_pkt record the packets lost for each links
        self.num_lost_pkt = 0.0

    def __lt__(self, other):
        return self.id < other.id

    # hosts and routers call this function to add their packets to this link
    def add_packet_to_buffer(self, pkt):
        if pkt.type != 'hello' and isinstance(self.start, router.Router):
            self.start.out_pkt_size[self.id] += pkt.size
        # drop tail algorithms
        if self.cur_size + pkt.size <= self.max_size:
            # add packet to buffer
            self.buffer.append(pkt)
            self.cur_size += pkt.size
            # for visualization purpose
            self.plot_link_buffer_time.append(global_var.timestamp)
            self.plot_link_buffer.append(self.cur_size/1024)
            # if link is idle, send the newly added packet immediately
            if self.link_lock == False:
                # create an event that specifies the time when this packet can move from buffer to on_the_link
                expected_waiting_time = pkt.size*8/(self.link_rate*1024*1024)
                cur_event = event_type.FetchFromBuffer(self, global_var.timestamp + expected_waiting_time)
                heapq.heappush(global_var.queue, cur_event)
                # link is not idle now
                self.link_lock = True
        else:
            # for debug purpose, lost one more packet on this link
            self.num_lost_pkt += 1

    # after pushing packet from buffer to link, packet will move from buffer to on_the_link
    def buffer_to_link(self):
        # create an event specifies when the packet can reach the destination
        cur_event = event_type.FetchFromLink(self, global_var.timestamp+self.link_delay)
        heapq.heappush(global_var.queue, cur_event)
        # move pkt from buffer to on_the_link
        pkt = self.buffer.popleft()
        self.cur_size -= pkt.size
        self.on_the_link.append(pkt)
        # if buffer is not empty, then send next packet in the buffer immediately
        if self.buffer:
            expected_waiting_time = self.buffer[0].size * 8 / (self.link_rate * 1024 * 1024)
            cur_event = event_type.FetchFromBuffer(self, global_var.timestamp + expected_waiting_time)
            heapq.heappush(global_var.queue, cur_event)
            # link is not idle
            self.link_lock = True
        else:
            # if buffer is empty, then the link will be idle
            self.link_lock = False

        # for plot purpose
        self.plot_link_buffer_time.append(global_var.timestamp)
        self.plot_link_buffer.append(self.cur_size / 1024)
        self.plot_link_rate_size += pkt.size

    # after the propagation delay, packets can move from on_the_link to destination
    def fetch_from_link(self):
        cur_pkt = self.on_the_link.popleft()
        # call destination to receive the packets
        self.end.receive_packet(cur_pkt, self)
