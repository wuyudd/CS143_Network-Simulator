from Router import Router
from Link import Link
from Host import Host


class Simulator():
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
            links[cur[0]] = Link(float(cur[1]), float(cur[2]), float(cur[3]), None, None)
            links[cur[0] + '*'] = Link(float(cur[1]), float(cur[2]), float(cur[3]), None, None)
            i += 1
        i += 1

        # read graph
        while i < len(data) and data[i] != '#':
            cur = data[i].split('\t')
            nodes[cur[1]].links.append(links[cur[0]])
            nodes[cur[2]].links.append(links[cur[0]])
            links[cur[0]].start = nodes[cur[1]]
            links[cur[0]].end = nodes[cur[2]]
            nodes[cur[1]].links.append(links[cur[0] + '*'])
            nodes[cur[2]].links.append(links[cur[0] + '*'])
            links[cur[0] + '*'].start = nodes[cur[2]]
            links[cur[0] + '*'].end = nodes[cur[1]]
            i += 1
        return nodes, links
    
    