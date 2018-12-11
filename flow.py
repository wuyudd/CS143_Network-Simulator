import heapq
import global_var
import copy
from host import *
from packet import *
from simulator import *
import event_type


class FlowState(object):
    # detect the threshold
    SLOWSTART_INIT = "ss0"
    # slow start
    SLOWSTART = "ss"
    # fast retransmit and fast recovery
    FRFR = "frfr"
    # congestion avoidance
    CA = "ca"

class Flow(object):
    def __init__(self, id, src, dest, size, start_time, packet_size, tcp_name):
        # flow ID
        self.id = id
        # the source of flow
        self.src = src
        # the destination of flow
        self.dest = dest
        # data amount
        self.size = size
        # start time
        self.start_time = start_time
        # all the packets generated by the flow
        self.pkt_pool = {}
        # packets waiting to be sent
        self.sending_queue = collections.deque()
        # packets need to be retransmitted immediately
        self.timeout_queue = collections.deque()
        # the number of packets generated by the flow
        self.total_number_of_packet = 0
        # the chosen tcp congestion algorithm
        self.tcp_name = tcp_name
        # whether receive a valid ack before time out
        self.recieve_ack_flag = False
        # expected timestamp for time out event, used to check if the time out event is canceled or validate
        self.expected_timeout = None
        # round trip time
        self.rtt = 0.2
        # if all the packets of the flow are sent successfully
        self.finished = 0
        
        # window size at every timestamp
        self.plot_window_size = []
        # timestamp for plot window size and round trip time
        self.plot_window_size_timestamp = []
        # round trip time at every timestamp
        self.plot_rtt = []


        # for reno initialization
        # current state of reno, initial state is slow start
        self.curr_state = FlowState.SLOWSTART_INIT
        # counter for duplicate ack
        self.num_dup_acks = 1
        # window size
        self.window_size = 1
        # previous window size
        self.prev_window_size = 0
        # if received three duplicate acks
        self.three_dup_flag = False
        # number of outstanding packets
        self.num_on_flight_pkt = 0
        # counter for duplicate acks
        self.dup_ack_count = 1
        # if the flow is time out
        self.timeout_flag = False
        # threshold
        self.ss_threshold = float('Inf')
        # last ack received
        self.last_ack = Packet(self.id+'pkt-1ack-1', "data_ack", global_consts.ACKSIZE, self.src, self.dest)  # zombie pkt

        # for fast_initialization
        # current state of FAST, initail state is congestion avoidance
        if tcp_name == 'FAST':
            self.curr_state = FlowState.CA
        # alpha for FAST
        self.FAST_ALPHA = 15
        # base round trip time
        self.FAST_BASE_RTT = -1
        # mark for update window size every other round trip time
        self.fast_window_size_update_flag = True
        # record current round trip time
        self.temp_rtt = 0

# Regular Function
    # generate packets of the flow
    def generate_packet(self):
        self.total_number_of_packet = int(self.size/global_consts.PACKETSIZE)
        print(self.total_number_of_packet)
        prefix = 'pkt'
        for i in range(self.total_number_of_packet):
            cur_pkt = Packet(self.id + prefix + str(i), 'data', global_consts.PACKETSIZE, self.src, self.dest)
            self.pkt_pool[prefix+str(i)] = cur_pkt
            self.sending_queue.append(cur_pkt)
        return

    # receive ack
    def receive_ack(self, ack):
        self.rtt = global_var.timestamp - ack.sending_time
        print('current rtt:' + str(self.rtt))
        print(str(global_var.timestamp) + ' ' + self.id + ':' + 'recieve ' + ack.id)
        # for congestion control choice
        self.plot_window_size_timestamp.append(global_var.timestamp)
        self.plot_window_size.append(self.window_size)
        self.plot_rtt.append(self.rtt)
        # determine if current flow is finished
        curr_ack_ind = int(ack.id.split('ack')[-1])
        if curr_ack_ind == self.total_number_of_packet:
            self.finished = 1

        if self.tcp_name == "Reno":
            self.tcp_reno(ack)
        elif self.tcp_name == "FAST":
            self.tcp_fast(ack)
        elif self.tcp_name == 'None':
            self.update_num_pkt_on_flight(ack)
            if self.flow_send_pkt():
                self.set_new_timeout()
            self.last_ack = ack
        return

    # send packets from source
    def flow_send_pkt(self):   # start_time & index
        send_flag = False
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        while self.timeout_queue and self.src.outgoing_links.cur_size < self.src.outgoing_links.max_size:
            pkt = self.timeout_queue.popleft()
            pkt.sending_time = global_var.timestamp
            self.src.send_packet(pkt)
            send_flag = True
        while self.sending_queue and self.num_on_flight_pkt + 1 <= self.window_size and not self.finished:
            pkt = self.sending_queue.popleft()
            pkt.sending_time = global_var.timestamp
            self.src.send_packet(pkt)
            self.num_on_flight_pkt += 1
            send_flag = True
        return send_flag

    # set time out event
    def set_new_timeout(self):
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        start_time = global_var.timestamp + self.rtt*2
        if not self.finished and self.expected_timeout != start_time:
            time_out_event = event_type.TimeOut(self, start_time)
            heapq.heappush(global_var.queue, time_out_event)
            self.recieve_ack_flag = False
            self.expected_timeout = start_time
        return

    # actions when the flow is time out
    def time_out(self, time):
        if self.finished:
            return
        if time == self.expected_timeout:
            print('+++++++++++++++++++++++TimeOut+++++++++++++++++++++')
            self.timeout_flag = True
            # retransmit last pkt immediately
            name = 'pkt' + self.last_ack.id.split('ack')[-1]
            retransmit_pkt = Packet(self.id + name, 'data', global_consts.PACKETSIZE, self.src, self.dest)
            self.timeout_queue.append(retransmit_pkt)

            if self.tcp_name == 'Reno':
                self.choose_reno_next_state()
                self.reno_action()
            elif self.tcp_name == 'FAST':
                self.choose_fast_next_state()
                self.fast_action()
            elif self.tcp_name == 'None':
                if self.flow_send_pkt():
                    self.set_new_timeout()
        return

    # TCP RENO
    def tcp_reno(self, ack):
        self.check_three_dup(ack)
        self.choose_reno_next_state()
        self.update_num_pkt_on_flight(ack)
        self.reno_action()
        self.last_ack = ack

        print(".............................................")
        print("timestamp: " + str(global_var.timestamp))
        print("current state: " + self.curr_state)
        print('outstanding/window:' + str(self.num_on_flight_pkt) + '/' + str(self.window_size))
        print("sending queue length: " + str(len(self.sending_queue)))
        print(".............................................")
        return

    def check_three_dup(self,ack):
        # get ack index of last ack and current ack
        cur_ack_ind = int(ack.id.split('ack')[-1])
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        # check duplicate ack
        # when encounter duplicate packages
        if cur_ack_ind == last_ack_ind:
            self.dup_ack_count += 1
            #when encounter 3 duplicates packages
            if self.dup_ack_count == 3:
                self.three_dup_flag = True
                # retransmit last pkt immediately
                name = 'pkt' + self.last_ack.id.split('ack')[-1]
                retransmit_pkt = Packet(self.id + name, 'data', global_consts.PACKETSIZE, self.src, self.dest)
                self.timeout_queue.append(retransmit_pkt)
        else:
            self.timeout_flag = False
            self.dup_ack_count = 1
            self.three_dup_flag = False
            self.recieve_ack_flag = True
        return

    # calculate the number of outstanding packets
    def update_num_pkt_on_flight(self, ack):
        cur_ack_ind = int(ack.id.split('ack')[-1])
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        self.num_on_flight_pkt -= cur_ack_ind - last_ack_ind
        return

    # send next packets and set new time out event when window size is enough
    def reno_action(self):
        if self.flow_send_pkt():
            self.set_new_timeout()
        return

    # state machine for reno
    def choose_reno_next_state(self):
        # we need to change the state, window size, ss_threshold here
        if self.curr_state == FlowState.SLOWSTART_INIT:
            if self.timeout_flag or self.three_dup_flag:
                self.curr_state = FlowState.SLOWSTART
                self.ss_threshold = max(self.window_size / 2, 2)
                self.window_size = 1
            else:
                self.window_size += 1
        elif self.curr_state == FlowState.SLOWSTART:
            if self.timeout_flag:
                # reminder: how to set timeout_flag
                self.curr_state = FlowState.SLOWSTART
                self.window_size = 1
            elif self.window_size >= self.ss_threshold:
                self.curr_state = FlowState.CA
            else:
                self.window_size += 1
        elif self.curr_state == FlowState.FRFR:
            # reminder: how to set three_dup_flag
            if self.three_dup_flag:
                self.curr_state = FlowState.FRFR
                self.window_size += 1
            else:
                self.curr_state = FlowState.CA
                self.window_size = self.prev_window_size/2
        elif self.curr_state == FlowState.CA:
            # reminder: how to set timeout_flag
            if self.three_dup_flag:
                self.curr_state = FlowState.FRFR
                self.prev_window_size = self.window_size
                self.window_size = self.window_size / 2 + 3
            elif self.timeout_flag:
                self.curr_state = FlowState.SLOWSTART
                self.ss_threshold = max(self.window_size / 2, 2)
                self.window_size = 1
            else:
                self.window_size += 1/self.window_size
        return

    # TCP FAST
    def tcp_fast(self, ack):
        curr_ack_ind = int(ack.id.split('ack')[-1])
        if curr_ack_ind == 1:
            self.fast_record_window_size()
        self.check_three_dup(ack)
        self.choose_fast_next_state()
        self.update_num_pkt_on_flight(ack)
        self.fast_action()
        self.last_ack = ack

        print(".............................................")
        print("timestamp: " + str(global_var.timestamp))
        print("current state: " + self.curr_state)
        print('outstanding/window:' + str(self.num_on_flight_pkt) + '/' + str(self.window_size))
        print("sending queue length: " + str(len(self.sending_queue)))
        print(".............................................")
        return

    # state machine for FAST
    def choose_fast_next_state(self):
        #we need to change the state, window size, ss_threshold here
        if self.curr_state == FlowState.SLOWSTART:
            if self.timeout_flag:
                # reminder: how to set timeout_flag
                self.curr_state = FlowState.SLOWSTART
                self.window_size = 1
            elif self.window_size >= self.FAST_ALPHA - 7:
                self.curr_state = FlowState.CA
            else:
                if self.fast_window_size_update_flag:
                    self.window_size += 1
        elif self.curr_state == FlowState.FRFR:
            # reminder: how to set three_dup_flag
            if self.three_dup_flag:
                self.curr_state = FlowState.FRFR
                self.window_size += 1
            else:
                self.curr_state = FlowState.CA
                self.window_size = self.prev_window_size/2
        elif self.curr_state == FlowState.CA:
            # initialization
            if self.FAST_BASE_RTT == -1:
                self.window_size = self.window_size + self.FAST_ALPHA
                self.FAST_BASE_RTT = self.rtt
                self.temp_rtt = self.rtt
            if self.three_dup_flag:
                self.curr_state = FlowState.FRFR
                self.prev_window_size = self.window_size
                self.window_size = self.window_size / 2 + 3
            elif self.timeout_flag:
                self.curr_state = FlowState.SLOWSTART
                self.window_size = 1
            else:
                if self.fast_window_size_update_flag:
                    self.window_size += self.FAST_BASE_RTT / self.temp_rtt - 1 + self.FAST_ALPHA / self.prev_window_size
                self.FAST_BASE_RTT = min(self.FAST_BASE_RTT, self.rtt)
        return

    # send next packets and set new time out event when window size is enough
    def fast_action(self):
        if self.flow_send_pkt():
            self.set_new_timeout()
        return

    # update round trip time and window size at beginning of every round trip time, used for distributing to small steps
    def fast_record_window_size(self):
        self.prev_window_size = self.window_size
        self.fast_window_size_update_flag = not self.fast_window_size_update_flag
        self.temp_rtt = self.rtt
        last_ack_ind = int(self.last_ack.id.split('ack')[-1])
        if not self.finished:
            new_event = event_type.FastRecordWindowSize(self, global_var.timestamp+self.rtt)
            heapq.heappush(global_var.queue, new_event)
        return