import heapq
import global_var
import copy
from host import *
from packet import *
from simulator import *
import event_type


class FlowState(object):
    RENOSLOWSTART_INIT = "ss0"
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
        self.packet_size = packet_size
        self.pkt_pool = {}
        self.ack_pool = {}
        self.sending_queue = collections.deque()
        self.timeout_queue = collections.deque()
        self.total_number_of_packet = 0
        self.tcp_name = tcp_name
        self.recieve_ack_flag = False
        self.expected_timeout = None

        self.num_dup_acks = 1
        self.plot_window_size = []
        self.prev_window_size = 0

        #for reno initialization
        self.curr_state = FlowState.RENOSLOWSTART_INIT
        self.window_size = 1
        self.three_dup_flag = False
        self.num_on_flight_pkt = 0
        self.ack_count = 1
        self.timeout_flag = False
        self.ss_threshold = float('Inf')
        self.last_ack = Packet(self.id+'pkt-1ack-1', "data_ack", global_consts.ACKSIZE, self.src, self.dest)  # zombie pkt
        #rtt
        self.rtt = 0.2

    def generate_packet(self):
        # ????????
        self.total_number_of_packet = int(self.size/self.packet_size)
        print(self.total_number_of_packet)
        prefix = 'pkt'
        for i in range(self.total_number_of_packet):
            cur_pkt = Packet(self.id + prefix + str(i), 'data', self.packet_size, self.src, self.dest)
            self.pkt_pool[prefix+str(i)] = cur_pkt
            self.ack_pool[cur_pkt.id] = False
            self.sending_queue.append(cur_pkt)
            # print(self.pkt_pool)
        return

    def receive_ack(self, ack):
        self.rtt = global_var.timestamp - ack.sending_time
        print('current rtt:' + str(self.rtt))
        print(str(global_var.timestamp) + ' ' + self.id + ':' + 'recieve ' + ack.id)
        self.recieve_ack_flag = True
        # for congestion control choice
        global_var.plot_window_size_pkt_timestamp.append(global_var.timestamp)
        self.plot_window_size.append(self.window_size)

        if self.tcp_name == "reno":
            self.tcp_reno(ack)
        if self.tcp_name == "fast":
            self.tcp_fast(ack)

    def flow_send_pkt(self):   # start_time & index
        send_flag = False
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        while self.timeout_queue and self.src.outgoing_links.cur_size < self.src.outgoing_links.max_size:
            pkt = self.timeout_queue.popleft()
            pkt.sending_time = global_var.timestamp
            self.src.send_packet(pkt)
            send_flag = True

        #this is for test
        # while self.timeout_queue:
        #      pkt = self.timeout_queue.popleft()
        #      pkt.sending_time = global_var.timestamp - 0.1
        #      self.dest.receive_packet(pkt, self.dest.incoming_links)
        #      send_flag = True

        while self.sending_queue and self.num_on_flight_pkt + 1 <= self.window_size and last_ack_ind != int(self.total_number_of_packet):
            pkt = self.sending_queue.popleft()
            pkt.sending_time = global_var.timestamp
            self.src.send_packet(pkt)
            self.num_on_flight_pkt += 1
            send_flag = True
        return send_flag

    def set_new_timeout(self):
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        start_time = global_var.timestamp + self.rtt*2
        if last_ack_ind != self.total_number_of_packet and self.expected_timeout != start_time:
            time_out_event = event_type.TimeOut(self, start_time)
            heapq.heappush(global_var.queue, time_out_event)
            self.recieve_ack_flag = False
            self.expected_timeout = start_time



    def time_out(self, time):
        if int(self.last_ack.id.split('ack')[-1]) == int(self.total_number_of_packet):
            return
        if time == self.expected_timeout:
            print('+++++++++++++++++++++++TimeOut+++++++++++++++++++++')
            if self.tcp_name == 'reno':
                self.timeout_flag = True
                name = 'pkt' + self.last_ack.id.split('ack')[-1]
                retransmit_pkt = Packet(self.id + name, 'data', self.packet_size, self.src, self.dest)
                self.timeout_queue.append(retransmit_pkt)
                self.choose_reno_next_state()
                if self.flow_send_pkt():
                    self.set_new_timeout()
                # if we cannot send current pkt immediately
                # then we need to keep checking if we can send the pkt

                # we need do more here
            elif self.tcp_name == 'fast':
                return


    def tcp_reno(self, ack):
        # get ack index of last ack and current ack
        cur_ack_ind = int(ack.id.split('ack')[-1])
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        #check duplicate ack
        if cur_ack_ind == last_ack_ind:
            self.ack_count += 1
            if self.ack_count == 3:
                self.three_dup_flag = True
                # retransmit last pkt immediately
                name = 'pkt' + self.last_ack.id.split('ack')[-1]
                retransmit_pkt = Packet(self.id + name, 'data', self.packet_size, self.src, self.dest)
                self.timeout_queue.append(retransmit_pkt)
        else:
            self.timeout_flag = False
            self.ack_count = 1
            self.three_dup_flag = False

        self.choose_reno_next_state()
        # ??????????????????????????????
        self.num_on_flight_pkt -= cur_ack_ind - last_ack_ind
        if self.flow_send_pkt():
            self.set_new_timeout()
        # 3 dup 强制发， 其他状态无所谓
        # if we cannot send current pkt immediately
        # then we need to keep checking if we can send the pkt

        self.last_ack = ack

        print(".............................................")
        print("timestamp: " + str(global_var.timestamp))
        # print("last ack id: " + self.last_ack.id)
        # print("current ack id: " + ack.id)
        print("current state: " + self.curr_state)
        print('outstanding/window:' + str(self.num_on_flight_pkt) + '/' + str(self.window_size))
        print("sending queue length: " + str(len(self.sending_queue)))
        # print("timeout queue length: " + str(len(self.timeout_queue)))
        print(".............................................")


    def choose_reno_next_state(self):
        # we need to change the state, window size, ss_threshold here
        if self.curr_state == FlowState.RENOSLOWSTART_INIT:
            if self.timeout_flag or self.three_dup_flag:
                self.curr_state = FlowState.RENOSLOWSTART
                self.ss_threshold = max(self.window_size / 2, 2)
                self.window_size = 1
            else:
                self.window_size += 1
        elif self.curr_state == FlowState.RENOSLOWSTART:
            # if self.three_dup_flag:
            #     self.curr_state = FlowState.RENOSLOWSTART
            #     # do we need to change the threshold here?????????
            #     #self.ss_threshold = self.window_size / 2
            #     self.window_size = 1
            #     # do we still need to keep updating the prev_window_size?
            #     #self.prev_window_size = self.window_size
            if self.timeout_flag:
                # reminder: how to set timeout_flag
                self.curr_state = FlowState.RENOSLOWSTART
                self.window_size = 1
            elif self.window_size >= self.ss_threshold:
                self.curr_state = FlowState.RENOCA
            else:
                self.window_size += 1

        elif self.curr_state == FlowState.RENOFRFR:
            # reminder: how to set three_dup_flag
            if self.three_dup_flag:
                self.curr_state = FlowState.RENOFRFR
                self.window_size += 1
            else:
                self.curr_state = FlowState.RENOCA
                self.window_size = self.prev_window_size/2

        elif self.curr_state == FlowState.RENOCA:
            # reminder: how to set timeout_flag
            if self.three_dup_flag:
                self.curr_state = FlowState.RENOFRFR
                self.prev_window_size = self.window_size
                self.window_size = self.window_size / 2 + 3
            elif self.timeout_flag:
                self.curr_state = FlowState.RENOSLOWSTART
                self.ss_threshold = max(self.window_size / 2, 2)
                self.window_size = 1
            else:
                self.window_size += 1/self.window_size