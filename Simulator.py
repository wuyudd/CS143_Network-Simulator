from Router import Router
from Link import Link
from Host import Host
from Node import Node


class Simulator():
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
            node[cur[1]].links.append(links[cur[0]])
            node[cur[2]].links.append(links[cur[0]])
            links[cur[0]].start = node[cur[1]]
            links[cur[0]].end = node[cur[2]]
            node[cur[1]].links.append(links[cur[0] + '*'])
            node[cur[2]].links.append(links[cur[0] + '*'])
            links[cur[0] + '*'].start = node[cur[2]]
            links[cur[0] + '*'].end = node[cur[1]]
            i += 1
