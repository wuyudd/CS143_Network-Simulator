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
        self.node = {}
        self.links = {}
        self.flow = {}

    def run(self):
        routers, hosts, links = self.build_graph('test1_temp.txt')
        self.display_graph(routers, hosts, links)
        flows = self.read_flow('flows.txt', hosts)

        event = event_type.SayHello(routers, hosts, -3)
        heapq.heappush(global_var.queue, event)
        event = event_type.UpdateRoutingInfo(routers, -2)
        heapq.heappush(global_var.queue, event)

        #links['L0'].max_size = 512*1024
        #links['L1'].link_rate = 12.5

        #H1 = hosts['H1']
        #H2 = hosts['H2']

        for i in range(1, 12):
            start_time = i * global_consts.UPDATEFREQUENCY
            event = event_type.UpdateRoutingInfo(routers, start_time)
            heapq.heappush(global_var.queue, event)

        for i in range(500):
            start_time = i * global_consts.READLINKRATEFREQUENCY
            event = event_type.CheckLinkRate(links, start_time)
            heapq.heappush(global_var.queue, event)
            global_var.plot_link_rate_time_axis.append(i * global_consts.READLINKRATEFREQUENCY)




        f = flows['F1']
        #routers['R1'].routing_table = {"10.10.10.1": links['L0*'], "10.10.10.2": links['L5']}
        #print(routers['R1'].incoming_links)
        #print(routers['R1'].outgoing_links)

        # deal with the flow, add event to queue
        #for f in flow:

        event_temp = event_type.FlowInitialize(f, f.start_time)
        heapq.heappush(global_var.queue, event_temp)
        # print(global_var.queue)

        while global_var.queue:
            event = heapq.heappop(global_var.queue)
            global_var.timestamp = event.start_time
            event.action()
            #print(event)
            #print(len(global_var.queue))
        for l in links.values():
            print(l.id+' delay: '+str(l.link_delay))
            print(l.id+' lost_pkt: '+str(l.num_lost_pkt))
        return links, flows


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
            links[cur[0]] = Link(cur[0], float(cur[1]), float(cur[2])*(10**-3), float(cur[3]), None, None)
            links[cur[0] + '*'] = Link(cur[0] + '*', float(cur[1]), float(cur[2])*(10**-3), float(cur[3]), None, None)
            i += 1
        i += 1

        # read graph
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            # specify the link from A to B
            # print(cur)
            endA,endB = cur[1],cur[2]
            if endA[0] == 'H' and endB[0] == 'H':
                node[endA].outgoing_links = links[cur[0]]
                node[endB].incoming_links = links[cur[0]]
                links[cur[0]].start = node[endA]
                links[cur[0]].end = node[endB]
                node[endA].incoming_links = links[cur[0] + '*']
                node[endB].outgoing_links = links[cur[0] + '*']
                links[cur[0] + '*'].start = node[endB]
                links[cur[0] + '*'].end = node[endA]

            elif endA[0] == 'H' and endB[0] == 'R':
                node[endA].outgoing_links = links[cur[0]]
                node[endB].incoming_links[cur[0]] = links[cur[0]]
                links[cur[0]].start = node[endA]
                links[cur[0]].end = node[endB]
                node[endA].incoming_links = links[cur[0] + '*']
                node[endB].outgoing_links[cur[0]+'*'] = links[cur[0] + '*']
                links[cur[0] + '*'].start = node[endB]
                links[cur[0] + '*'].end = node[endA]

            elif endA[0] == 'R' and endB[0] == 'H':
                node[endA].outgoing_links[cur[0]] = links[cur[0]]
                node[endB].incoming_links = links[cur[0]]
                links[cur[0]].start = node[endA]
                links[cur[0]].end = node[endB]
                node[endA].incoming_links[cur[0] + '*'] = links[cur[0] + '*']
                node[endB].outgoing_links = links[cur[0] + '*']
                links[cur[0] + '*'].start = node[endB]
                links[cur[0] + '*'].end = node[endA]

            elif endA[0] == 'R' and endB[0] == 'R':
                node[endA].outgoing_links[cur[0]] = links[cur[0]]
                node[endB].incoming_links[cur[0]] = links[cur[0]]
                links[cur[0]].start = node[endA]
                links[cur[0]].end = node[endB]
                node[endA].incoming_links[cur[0] + '*'] = links[cur[0] + '*']
                node[endB].outgoing_links[cur[0] + '*'] = links[cur[0] + '*']
                links[cur[0] + '*'].start = node[endB]
                links[cur[0] + '*'].end = node[endA]

            i += 1

        routers = {}
        hosts = {}
        for key in node.keys():
            if key[0] == 'H':
                hosts[key] = node[key]
            elif key[0] == 'R':
                routers[key] = node[key]
        return routers, hosts, links


    def read_flow(self, file_name, hosts):
        data = [line.strip('\n') for line in open(file_name, 'r')]
        #print(data)
        flows = {}
        i = 0
        while i < len(data):
            cur = data[i].split('\t')
            #print(cur)
            flows[cur[0]] = Flow(cur[0], hosts[cur[1]], hosts[cur[2]], float(cur[3]), float(cur[4]), global_consts.PACKETSIZE, "reno")
            hosts[cur[1]].flows[cur[0]] = flows[cur[0]]
            i += 1
        return flows

    def display_graph(self,routers, hosts, links):
        for link in links.values():
            print(link.id+': '+link.start.id+'->'+link.end.id)
            print(link.id+' link rate: '+str(link.link_rate))
