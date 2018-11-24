import global_var
from event import *
from router import *
from simulator import *
import heapq


class FlowInitialize(Event):
    def __init__(self, flow, start_time):
        self.flow = flow;
        self.start_time = start_time

    def action(self):
        self.flow.generate_packet()
        self.flow.add_event()


class SendFromFlow(Event):
    def __init__(self, flow, index, start_time):
        self.flow = flow
        self.index = index
        self.start_time = start_time

    def action(self):
        prefix = 'pkt'
        packet = self.flow.pkt_pool[prefix + str(self.index)]
        self.flow.send_packet(packet)


class FetchFromBuffer(Event):
    def __init__(self, link, start_time):
        self.link = link
        self.start_time = start_time

    def action(self):
        self.link.buffer_to_link()


class FetchFromLink(Event):
    def __init__(self, link, start_time):
        self.link = link
        self.start_time = start_time

    def action(self):
        self.link.fetch_from_link()


class TimeOut(Event):
    def __init__(self, pkt, flow, start_time):
        self.pkt = pkt
        self.flow = flow
        self.start_time = start_time

    def action(self):
        # host check ACK
        # if TimeOut, change window size and send again
        #global_var.queue.append(SendPkt())
        # if not Timeout, end
        self.flow.time_out(self.pkt)


class UpdateRoutingInfo(Event):
    def __init__(self, routers, start_time):
        self.routers = routers
        self.start_time = start_time

    def action(self):
        global_var.updating_flag = True
        for router in self.routers.values():
            router.broadcast_routing_pkt()

        event = UpdateRoutingTable(self.routers, self.start_time + global_consts.UPDATEDURATION)
        heapq.heappush(global_var.queue, event)


class UpdateRoutingTable(Event):
    def __init__(self, routers, start_time):
        self.routers = routers
        self.start_time = start_time

    def action(self):
        for router in self.routers.values():
            router.dijkstra()

            # dijkstra
        global_var.updating_flag = False
        global_var.period += 1

class CheckLinkRate(Event):
    def __init__(self, links, start_time):
        self.links = links
        self.start_time = start_time

    def action(self):
        for link in self.links.values():
            link.plot_link_rate.append(link.plot_link_rate_size / global_consts.READLINKRATEFREQUENCY)
            link.plot_link_rate_size = 0


class SayHello(Event):
    def __init__(self, routers, hosts, start_time):
        self.routers = routers
        self.hosts = hosts
        self.start_time = start_time

    def action(self):
        for router in self.routers.values():
            router.say_hello()

        for host in self.hosts.values():
            host.say_hello()

""""

class RunDijkstra(Event):
    def __init__(self, routers, nodes):
        self.routers = routers
        self.nodes = nodes

    def action(self):
        for router in self.routers:
            counter = 0
            queue = [] # save links by comparing weight, (weight, outgoing_link)
            curr_router = router
            curr_router_link_list = {curr_router.id: []} # the shortest path from router to curr_router
            num_of_hosts = len(self.nodes) - len(self.routers) # number of hosts
            while counter < num_of_hosts:
                while isinstance(curr_router, Host):
                    # at this time, curr_router is a host instance
                    if counter < num_of_hosts:
                        router.routing_table[curr_router.id] = curr_router_link_list[0] # only need the link from router
                        curr_router = queue.pop()[1].end
                        counter += 1
                    else:
                        break
                curr_router_outgoing_links = curr_router.outgoing_links
                for curr_router_outgoing_link in curr_router_outgoing_links:
                    curr_router_end = curr_router_outgoing_link.end
                    if (self.id, curr_router_end.id) in curr_router.map:
                        curr_router_outgoing_link_weight = curr_router.map[(self.id, curr_router_end.id)] # get weight from map of curr_router
                        heapq.heappush(queue, (curr_router_outgoing_link_weight, curr_router_outgoing_link))

                curr_min_link = heapq.heappop(queue)[1]
                curr_router_link_list[curr_router.end.id] = curr_router_link_list[curr_router.id].append(curr_min_link)
                curr_router = curr_min_link.end

"""