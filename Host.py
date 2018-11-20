from Node import Node


class Host(Node):
    def __init__(self, host_ipaddr, connected_link):
        self.id = host_ipaddr
        super().__init__(connected_link)

    def send(self, to_send_pkt):
        self.links.add_pkg_to_buffer_in(to_send_pkt)

    def receive(self):
        return self.links.pick_pkg_from_buffer_out()
