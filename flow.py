import heapq
import global_var
import copy
from host import *
from packet import *
from simulator import *
import event_type


class FlowState(object):
    RENOSLOWSTART = 0
    RENOTIMEOUTSLOWSTART = 1
    RENOFRFR = 2
    RENOCA = 3


class Flow(object):
    def __init__(self, id, src, dest, size, start_time, packet_size, tcp_name):
        self.id = id
        self.src = src
        self.dest = dest
        self.size = size
        self.start_time = start_time
        self.cnt = 0
        self.window_size = 64
        self.packet_size = packet_size
        self.pkt_pool = {}
        self.ack_pool = {}
        self.sending_queue = collections.deque()
        self.timeout_queue = collections.deque()
        self.num_pkt_send = 0
        self.last_send_time = start_time
        self.tcp_name = tcp_name

        self.expected_timeout = None
        self.ack_num = 0
        # for reno
        self.ss_threshold = 5
        self.last_ack = Packet('0', "data_ack", 1024, '10.10.10.1', '10.10.10.2') # zombie pkt
        self.curr_state = FlowState.RENOSLOWSTART
        self.num_dup_acks = 0



    def generate_packet(self):
        number_of_packet = int(self.size/self.packet_size)
        prefix = 'pkt'
        for i in range(number_of_packet):
            # pkt: id, type, size, end1, end2, pos
            cur_pkt = Packet(self.id + prefix + str(i), 'data', self.packet_size, self.src, self.dest)
            self.pkt_pool[prefix+str(i)] = cur_pkt
            self.ack_pool[cur_pkt.id] = False
            self.sending_queue.append(cur_pkt)
            # print(self.pkt_pool)
        return

    # def send_packet(self,pkt):
    #     self.src.send_packet(pkt)
    #     event = event_type.TimeOut(pkt, self, global_var.timestamp+2) # constant need to be modified
    #     heapq.heappush(global_var.queue, event)
    #     return

    def receive_ack(self, ack):
        pkt_name = ack.id.split('ack')[0]
        self.ack_pool[pkt_name] = True  # find the packet and mark it acknowledged
        self.cnt -= 1
        self.ack_num += 1
        self.add_event()
        self.last_ack = ack
        print(ack.id)


        # for congestion control choice

        # if self.tcp_name == "reno":
        #     self.tcp_reno(ack)
        #
        # if self.tcp_name == "fast":
        #     self.tcp_fast(ack)

    def add_event(self):   # start_time & index
        send_flag = False
        while self.timeout_queue and self.cnt < self.window_size:
            pkt = self.timeout_queue.popleft()
            self.src.send_packet(pkt)
            self.cnt += 1
            send_flag = True
        while self.sending_queue and self.cnt < self.window_size:
            pkt = self.sending_queue.popleft()
            self.src.send_packet(pkt)
            # event = event_type.SendFromFlow(self, pkt, global_var.timestamp)
            self.cnt += 1
            send_flag = True
        if send_flag:
            start_time = global_var.timestamp + 0.2
            time_out_event = event_type.TimeOut(self, start_time)
            heapq.heappush(global_var.queue, time_out_event)
            self.expected_timeout = start_time

    def time_out(self):
        print('+++++++++++++++++++++++TimeOut+++++++++++++++++++++')
        ind = self.last_ack.id.split('ack')[-1]
        name = 'pkt' + ind
        retransmit_pkt = Packet(self.id + name, 'data', self.packet_size, self.src, self.dest)
        self.timeout_queue.append(retransmit_pkt)
        self.add_event()

        # if not self.ack_pool[pkt.id]:
        #     self.cnt -= 1   # need to resend pck
        #     new_pkt = Packet(pkt.id, pkt.type, pkt.size, pkt.start, pkt.end)
        #     self.timeout_queue.append(new_pkt)
        #     self.add_event()

            # for reno
            #self.ss_threshold = self.window_size / 2
            #self.window_size = 1
            #self.curr_state = FlowState.RENOSLOWSTART

    def tcp_reno(self, ack):
        if self.curr_state == FlowState.RENOSLOWSTART:
                self.slow_start(ack)
        elif self.curr_state == FlowState.RENOCA:
            self.congestion_avoid(ack)
        elif self.curr_state == FlowState.RENOFRFR:
            self.fr_fr(ack)
    
        self.last_ack = ack

    def slow_start(self, ack):
        if self.window_size < self.ss_threshold:
            self.window_size += 1
        else:
            self.curr_state = FlowState.RENOCA

    def congestion_avoid(self, ack):
        if ack.id != self.last_ack.id:
            self.window_size += 1 / self.window_size
        else:
            self.dup_acks_cnt(ack)

    def fr_fr(self, ack):
        self.ss_threshold = max(self.window_size / 2, 2)
        #self.retransmit(ack)
        self.window_size = self.ss_threshold + 3
        if ack.id == self.last_ack.id:
            self.window_size += 1
        else:
            self.curr_state = FlowState.RENOCA
            self.window_size = self.ss_threshold / 2
            self.num_dup_acks = 0

    def dup_acks_cnt(self, ack):
        self.num_dup_acks += 1
        if self.num_dup_acks == 3:
            # retransmit immediately
            # self.id + "pkt" + str(pkt.id.split("ack")[1])
            retransmit_pkt = Packet(self.id + "pkt" + str(ack.id.split("ack")[1]), "data", global_consts.PACKETSIZE, ack.end, ack.start)
            self.timeout_queue.append(retransmit_pkt)
            self.add_event()
            self.curr_state = FlowState.RENOFRFR

    # def tcp_fast(self, pkt):