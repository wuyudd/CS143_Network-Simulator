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
        self.ss_threshold = float('Inf')
        self.last_ack = Packet('0', "data_ack", 1024, '10.10.10.1', '10.10.10.2') # zombie pkt
        self.curr_state = FlowState.RENOSLOWSTART
        self.num_dup_acks = 1
        self.plot_window_size = []
        self.prev_ca_window_size = 0

        #rtt 

    def generate_packet(self):
        # ????????
        self.total_number_of_packet = int(self.size/self.packet_size)
        print(self.total_number_of_packet)
        prefix = 'pkt'
        for i in range(self.total_number_of_packet):
            # pkt: id, type, size, end1, end2, pos
            cur_pkt = Packet(self.id + prefix + str(i), 'data', self.packet_size, self.src, self.dest)
            self.pkt_pool[prefix+str(i)] = cur_pkt
            self.ack_pool[cur_pkt.id] = False
            self.sending_queue.append(cur_pkt)
            # print(self.pkt_pool)
        return

    def receive_ack(self, ack):
        #print(str(global_var.timestamp) + ' ' + self.id + ':' + 'recieve ' + ack.id)
        self.recieve_ack_flag = True
        pkt_name = ack.id.split('ack')[0]
        if self.ack_pool[pkt_name] == False:
            self.cnt -= 1
        self.ack_pool[pkt_name] = True  # find the packet and mark it acknowledged
        self.flow_send_pkt()
        self.set_new_timeout()

        # for congestion control choice
        global_var.plot_window_size_pkt_timestamp.append(global_var.timestamp)
        self.plot_window_size.append(self.window_size)
        if self.tcp_name == "reno":
            self.tcp_reno(ack)
        if self.tcp_name == "fast":
            self.tcp_fast(ack)

    def flow_send_pkt(self):   # start_time & index
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        while self.sending_queue and self.cnt + 1 <= self.window_size and last_ack_ind != int(self.total_number_of_packet):
            pkt = self.sending_queue.popleft()
            self.src.send_packet(pkt)
            self.cnt += 1

    def set_new_timeout(self):
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        start_time = global_var.timestamp + 0.2
        if last_ack_ind != self.total_number_of_packet and self.expected_timeout != start_time:
            time_out_event = event_type.TimeOut(self, start_time)
            heapq.heappush(global_var.queue, time_out_event)
            self.recieve_ack_flag = False
            self.expected_timeout = start_time


    def time_out(self):
        print('+++++++++++++++++++++++TimeOut+++++++++++++++++++++')
        #print(len(self.timeout_queue))
        if int(self.last_ack.id.split('ack')[-1]) == int(self.total_number_of_packet):
            return
        name = 'pkt' + self.last_ack.id.split('ack')[-1]
        retransmit_pkt = Packet(self.id + name, 'data', self.packet_size, self.src, self.dest)
        #self.timeout_queue.append(retransmit_pkt)
        self.src.send_packet(retransmit_pkt)
        self.set_new_timeout()
        #for reno
        self.ss_threshold = self.window_size / 2
        self.window_size = 1
        self.curr_state = FlowState.RENOSLOWSTART

        # 一共128个包， W = 128 ACK64收到了， 然后没包发 触发不了Reno？



    def tcp_reno(self, ack):
        print(".............................................")
        print("last ack id: " + self.last_ack.id)
        print("current ack id: " + ack.id)
        print("current state: " + self.curr_state)
        print("timestamp: " + str(global_var.timestamp) + ' window/outstanding:' + str(self.window_size) + '/' + str(self.cnt))
        print("sending queue length: " + str(len(self.sending_queue)))
        print("timeout queue length: " + str(len(self.timeout_queue)))
        print(".............................................")

        if self.curr_state == FlowState.RENOSLOWSTART:
            self.slow_start(ack)
        elif self.curr_state == FlowState.RENOCA:
            self.congestion_avoid(ack)
        elif self.curr_state == FlowState.RENOFRFR:
            self.fr_fr(ack)
        self.last_ack = ack

    # under construction
    def slow_start(self, ack):
        if ack.id.split("ack")[-1] == self.last_ack.id.split("ack")[-1]:
            self.dup_acks_cnt(ack)
        else:
            self.num_dup_acks = 1

    #under construction
    def congestion_avoid(self, ack):
        if ack.id.split("ack")[-1] != self.last_ack.id.split("ack")[-1]: # 命名对应要改
            self.num_dup_acks = 1
            self.window_size += 1 / self.window_size
            self.flow_send_pkt()
        else:
            self.dup_acks_cnt(ack)

    # under construction
    def fr_fr(self, ack):
        if ack.id.split("ack")[-1] == self.last_ack.id.split("ack")[-1]:
            self.window_size += 1
        else:
            self.curr_state = FlowState.RENOCA
            self.window_size = self.prev_ca_window_size/2
            self.num_dup_acks = 1


    def dup_acks_cnt(self, ack):
        self.num_dup_acks += 1
        if self.num_dup_acks == 3:
            # retransmit immediately
            print("3 dup acks !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.curr_state = FlowState.RENOFRFR
            retransmit_pkt = Packet(self.id + "pkt" + str(ack.id.split("ack")[1]), "data", global_consts.PACKETSIZE, ack.end, ack.start)
            self.src.send_packet(retransmit_pkt)
            self.set_new_timeout()
            self.prev_ca_window_size = self.window_size
            self.window_size = 1/2*self.window_size + 3
            

    # def tcp_fast(self, pkt):