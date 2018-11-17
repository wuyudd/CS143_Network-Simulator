from packet import Packet
from link import Link


class Host(object):
    def __init__(self, host_ipaddr, connected_link):
        self.__id = host_ipaddr
        self.__link = connected_link

    def send(self, to_send_pkt):
        self.link.add_pkg_to_buffer_in(to_send_pkt)

    def receive(self):
        return self.link.pick_pkg_from_buffer_out()
