from Router import Router
from Link import Link
from Host import Host
from Node import Node
import heapq
import EventType


class Simulator():
    queue = []
    timestamp = 0.0
    flow = {}

    def __init__(self):
        self.node = {}
        self.links = {}
        self.flow = {}
        self.queue = []
        self.timestamp = 0.0

    def run(self):
        # node, links = self.build_graph()
        flow = self.import_flow()

        # deal with the flow, add event to queue
        for f in flow:
            event_temp = EventType.FlowInitialize(f, f.start_time)
            heapq.heappush(Simulator.queue, (f.start_time, event_temp))

        while Simulator.queue:
            event = heapq.heappop(Simulator.queue)
            event.action()

    def import_flow(self):
        return self

    def build_graph(self, file_name):
        data = [line.strip('\n') for line in open(file_name, 'r')]
        i = 1
        node = {}
        links = {}
        # print(data)
        # read host
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            node[cur[0]] = Host(cur[1])
            i += 1
        i += 1

        # read router
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            node[cur[0]] = Router(cur[0])
            i += 1
        i += 1

        # read link
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            links[cur[0]] = Link(cur[0], float(cur[1]), float(cur[2]), float(cur[3]), None, None)
            links[cur[0] + '*'] = Link(cur[0] + '*', float(cur[1]), float(cur[2]), float(cur[3]), None, None)
            i += 1
        i += 1

        # read graph
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            # specify the link from A to B
            node[cur[1]].outgoing_links.append(links[cur[0]])
            node[cur[2]].incoming_links.append(links[cur[0]])
            links[cur[0]].start = node[cur[1]]
            links[cur[0]].end = node[cur[2]]

            # specify the link from B to A
            node[cur[1]].incoming_links.append(links[cur[0] + '*'])
            node[cur[2]].outgoing_links.append(links[cur[0] + '*'])
            links[cur[0] + '*'].start = node[cur[2]]
            links[cur[0] + '*'].end = node[cur[1]]
            i += 1
