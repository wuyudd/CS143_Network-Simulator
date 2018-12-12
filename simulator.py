"""
simulator.py is to build graph from the test case file and also read flows.
"""
from router import *
from link import *
from host import *
from node import *
from flow import *
import heapq
import event_type
import global_var
import global_consts


class Simulator(object):
    def __init__(self):
        # they are the main component of simulations
        # nodes is a map which contains each node: key is the name of host/router and value is the instance of host/router
        self.nodes = {}
        # links is a map which contains each link: key is the name of link and value is the instance of host/router
        self.links = {}
        # links is a map which contains each flow: key is the name of flow and value is the instance of flow
        self.flows = {}
    # simulation takes in the graph_file(network structure) and flow_file(flows information)

    def run(self, graph_file_name, flow_file_name):
        # from the graph file, call build_graph function to reconstruct the network structure
        routers, hosts, links = self.build_graph(graph_file_name)
        # for debug purpose, shows full layout of the newtwork structure
        self.display_graph(routers, hosts, links)
        # from flows file, call read_flow to build flow instances
        flows = self.read_flow(flow_file_name, hosts)

        # initialization of the routers, let each router knows its neighbors
        event = event_type.SayHello(routers, hosts, -3)
        heapq.heappush(global_var.queue, event)
        # update the information for routing
        event = event_type.UpdateRoutingInfo(routers, -2)
        heapq.heappush(global_var.queue, event)
        # initialization of check-link-rate event
        event = event_type.CheckLinkRate(links, 0)
        heapq.heappush(global_var.queue, event)

        # deal with the flow, initialize each flows
        for name, f in flows.items():
            event_temp = event_type.FlowInitialize(f, f.start_time)
            heapq.heappush(global_var.queue, event_temp)

        # run the whole process
        while global_var.queue:
            # run the event one by one
            event = heapq.heappop(global_var.queue)
            global_var.timestamp = event.start_time
            event.action()

            # following determines if all flows are end
            # if all flows end: no need to add check-link-rate event or update-routing-info event
            # if there is one flow still going one: still need to add check-link-rate event or update-routing-info event
            if isinstance(event, event_type.UpdateRoutingInfo) or isinstance(event, event_type.CheckLinkRate):
                all_finished_sum = 0
                for flow_id, cur_flow in flows.items():
                    all_finished_sum += cur_flow.finished
                if all_finished_sum != len(flows):
                    if isinstance(event, event_type.UpdateRoutingInfo):
                        new_event = event_type.UpdateRoutingInfo(routers, global_var.timestamp + global_consts.UPDATEFREQUENCY)
                        heapq.heappush(global_var.queue, new_event)
                    elif isinstance(event, event_type.CheckLinkRate):
                        new_event = event_type.CheckLinkRate(links, global_var.timestamp + global_consts.READLINKRATEFREQUENCY)
                        heapq.heappush(global_var.queue, new_event)

        # for debug, output the number of packets lost for each link
        for l in links.values():
            print(l.id+' lost_pkt: '+str(l.num_lost_pkt))
        return links, flows

    # This function read the txt file and construct the graph structure
    def build_graph(self, file_name):
        data = [line.strip('\n') for line in open(file_name, 'r')]
        i = 1
        nodes = {}
        links = {}

        # read host
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            nodes[cur[0]] = Host(cur[1])
            i += 1
        i += 1

        # read router
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            nodes[cur[0]] = Router(cur[0])
            i += 1
        i += 1

        # read link
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            links[cur[0]] = Link(cur[0], float(cur[1]), float(cur[2])*(10**-3), float(cur[3]), None, None)
            links[cur[0] + '*'] = Link(cur[0] + '*', float(cur[1]), float(cur[2])*(10**-3), float(cur[3]), None, None)
            i += 1
        i += 1
        # read graph
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            # specify the link from A to B
            endA,endB = cur[1],cur[2]
            if endA[0] == 'H' and endB[0] == 'H':
                nodes[endA].outgoing_links = links[cur[0]]
                nodes[endB].incoming_links = links[cur[0]]
                links[cur[0]].start = nodes[endA]
                links[cur[0]].end = nodes[endB]
                nodes[endA].incoming_links = links[cur[0] + '*']
                nodes[endB].outgoing_links = links[cur[0] + '*']
                links[cur[0] + '*'].start = nodes[endB]
                links[cur[0] + '*'].end = nodes[endA]

            elif endA[0] == 'H' and endB[0] == 'R':
                nodes[endA].outgoing_links = links[cur[0]]
                nodes[endB].incoming_links[cur[0]] = links[cur[0]]
                links[cur[0]].start = nodes[endA]
                links[cur[0]].end = nodes[endB]
                nodes[endA].incoming_links = links[cur[0] + '*']
                nodes[endB].outgoing_links[cur[0]+'*'] = links[cur[0] + '*']
                links[cur[0] + '*'].start = nodes[endB]
                links[cur[0] + '*'].end = nodes[endA]

            elif endA[0] == 'R' and endB[0] == 'H':
                nodes[endA].outgoing_links[cur[0]] = links[cur[0]]
                nodes[endB].incoming_links = links[cur[0]]
                links[cur[0]].start = nodes[endA]
                links[cur[0]].end = nodes[endB]
                nodes[endA].incoming_links[cur[0] + '*'] = links[cur[0] + '*']
                nodes[endB].outgoing_links = links[cur[0] + '*']
                links[cur[0] + '*'].start = nodes[endB]
                links[cur[0] + '*'].end = nodes[endA]

            elif endA[0] == 'R' and endB[0] == 'R':
                nodes[endA].outgoing_links[cur[0]] = links[cur[0]]
                nodes[endB].incoming_links[cur[0]] = links[cur[0]]
                links[cur[0]].start = nodes[endA]
                links[cur[0]].end = nodes[endB]
                nodes[endA].incoming_links[cur[0] + '*'] = links[cur[0] + '*']
                nodes[endB].outgoing_links[cur[0] + '*'] = links[cur[0] + '*']
                links[cur[0] + '*'].start = nodes[endB]
                links[cur[0] + '*'].end = nodes[endA]

            i += 1

        routers = {}
        hosts = {}
        for key in nodes.keys():
            if key[0] == 'H':
                hosts[key] = nodes[key]
            elif key[0] == 'R':
                routers[key] = nodes[key]
        return routers, hosts, links

    # This function read the txt file and construct the flows
    def read_flow(self, file_name, hosts):
        data = [line.strip('\n') for line in open(file_name, 'r')]
        flows = {}
        i = 0
        while i < len(data):
            cur = data[i].split('\t')
            flows[cur[0]] = Flow(cur[0], hosts[cur[1]], hosts[cur[2]], float(cur[3]), float(cur[4]), global_consts.PACKETSIZE, cur[5])
            hosts[cur[1]].flows[cur[0]] = flows[cur[0]]
            i += 1
        return flows

    # This function display the connection of the graph
    def display_graph(self,routers, hosts, links):
        for link in links.values():
            print(link.id+': '+link.start.id+'->'+link.end.id)
            print(link.id+' link rate: '+str(link.link_rate))
