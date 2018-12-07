import heapq
import global_var
import copy
from host import *
from packet import *
from simulator import *
import event_type


class FlowState(object):
    RENOSLOWSTART = "ss"
    RENOTIMEOUTSLOWSTART = "to"
    RENOFRFR = "frfr"
    RENOCA = "ca"


class Flow(object):
    def __init__(self, id, src, dest, size, start_time, packet_size, tcp_name):
        self.id = id
        self.src = src
        self.dest = dest
        self.size = size
        self.start_time = start_time
        self.cnt = 0
        self.window_size = 1
        self.packet_size = packet_size
        self.pkt_pool = {}
        self.ack_pool = {}
        self.sending_queue = collections.deque()
        self.timeout_queue = collections.deque()
        self.total_number_of_packet = 0
        self.num_pkt_send = 0
        self.last_send_time = start_time
        self.tcp_name = tcp_name
        self.recieve_ack_flag = False

        self.expected_timeout = None
        # for reno
        self.ss_threshold = 40
        self.last_ack = Packet('0', "data_ack", 1024, '10.10.10.1', '10.10.10.2') # zombie pkt
        self.curr_state = FlowState.RENOSLOWSTART
        self.num_dup_acks = 0
        self.plot_window_size = []

    def generate_packet(self):
        # ????????
        self.total_number_of_packet = int(self.size/self.packet_size)
        #print(self.total_number_of_packet)
        prefix = 'pkt'
        for i in range(self.total_number_of_packet):
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
        print(str(global_var.timestamp) + ' ' + self.id + ':' + 'recieve ' + ack.id)
        self.recieve_ack_flag = True
        #self.last_ack = ack
        pkt_name = ack.id.split('ack')[0]
        self.ack_pool[pkt_name] = True  # find the packet and mark it acknowledged
        self.cnt -= 1
        self.add_event()

        # for congestion control choice
        global_var.plot_window_size_pkt_timestamp.append(global_var.timestamp)
        self.plot_window_size.append(self.window_size)
        if self.tcp_name == "reno":
            self.tcp_reno(ack)

        if self.tcp_name == "fast":
            self.tcp_fast(ack)


    def add_event(self):   # start_time & index
        #send_flag = False
        print(len(self.timeout_queue))
        print(len(self.sending_queue))
        print(self.cnt)
        print(self.window_size)
        while self.timeout_queue and self.cnt + 1 <= self.window_size: # ! ??
            pkt = self.timeout_queue.popleft()
            self.src.send_packet(pkt)
            self.cnt += 1
            #send_flag = True
        while self.sending_queue and self.cnt + 1 <= self.window_size:
            pkt = self.sending_queue.popleft()
            self.src.send_packet(pkt)
            self.cnt += 1
            #send_flag = True

        if self.cnt != 0:
            start_time = global_var.timestamp + 0.2
            time_out_event = event_type.TimeOut(self, start_time)
            heapq.heappush(global_var.queue, time_out_event)
            self.recieve_ack_flag = False
            self.expected_timeout = start_time

    def time_out(self):
        print('+++++++++++++++++++++++TimeOut+++++++++++++++++++++')
        print(len(self.timeout_queue))
        if int(self.last_ack.id.split('ack')[-1]) == int(self.total_number_of_packet):
            return
        last_lost_pkt_ind = int(self.last_ack.id.split('ack')[-1])
        upper_bound = 0
        if self.sending_queue:
            upper_bound = int(self.sending_queue[0].id.split('pkt')[-1])
        else:
            upper_bound = self.total_number_of_packet
        #print(upper_bound)
        while last_lost_pkt_ind < upper_bound:
            name = 'pkt' + str(last_lost_pkt_ind)
            retransmit_pkt = Packet(self.id + name, 'data', self.packet_size, self.src, self.dest)
            self.timeout_queue.append(retransmit_pkt)
            last_lost_pkt_ind += 1
        print(len(self.timeout_queue))
        self.add_event()

        # for reno
        self.ss_threshold = self.window_size / 2
        self.window_size = 1
        self.curr_state = FlowState.RENOSLOWSTART
        self.cnt = 0

        # 一共128个包， W = 128 ACK64收到了， 然后没包发 触发不了Reno？

    def tcp_reno(self, ack):
        print(".............................................")
        print(self.last_ack.id)
        print(ack.id)
        print("current state: " + self.curr_state)
        print(str(global_var.timestamp) + ' window/outstanding:' + str(self.window_size) + '/' + str(self.cnt))
        print("sending queue length: ")
        print(len(self.sending_queue))
        print("timeout queue length: ")
        print(len(self.timeout_queue))
        print(".............................................")

        if self.curr_state == FlowState.RENOSLOWSTART:
                self.slow_start(ack)
        elif self.curr_state == FlowState.RENOCA:
            self.congestion_avoid(ack)
        elif self.curr_state == FlowState.RENOFRFR:
            self.fr_fr(ack)

        self.last_ack = ack

    def slow_start(self, ack):
        if ack.id.split("ack")[-1] != self.last_ack.id.split("ack")[-1]:
            self.num_dup_acks = 0
            if self.window_size < self.ss_threshold:
                self.window_size += 1
                self.add_event()
            elif self.window_size == self.ss_threshold:
                self.add_event()
                self.curr_state = FlowState.RENOCA
        else:
            self.dup_acks_cnt(ack)

    def congestion_avoid(self, ack):
        if ack.id.split("ack")[-1] != self.last_ack.id.split("ack")[-1]: # 命名对应要改
            self.num_dup_acks = 0
            self.window_size += 1 / self.window_size
            self.add_event()
        else:
            self.dup_acks_cnt(ack)

    def fr_fr(self, ack):
        if ack.id.split("ack")[-1] == self.last_ack.id.split("ack")[-1]:
            self.window_size += 1
            self.add_event()
        else:
            self.curr_state = FlowState.RENOCA
            self.window_size = self.ss_threshold / 2
            self.num_dup_acks = 0

    def dup_acks_cnt(self, ack):
        self.num_dup_acks += 1
        if self.num_dup_acks == 3:
            # retransmit immediately
            # self.id + "pkt" + str(pkt.id.split("ack")[1])
            print("3 dup acks !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            retransmit_pkt = Packet(self.id + "pkt" + str(ack.id.split("ack")[1]), "data", global_consts.PACKETSIZE, ack.end, ack.start)
            self.timeout_queue.append(retransmit_pkt)
            self.add_event()
            self.curr_state = FlowState.RENOFRFR

            self.ss_threshold = max(self.window_size / 2, 2)
            self.window_size = self.ss_threshold + 3

    # def tcp_fast(self, pkt):