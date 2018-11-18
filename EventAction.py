import Host
import Link

class EventAction(object):
    FLOWTOHOST = 0
    HOSTTOLINK = 1
    LINKTRANSMIT = 2
    LINKTOHOST = 3

    def __init__(self):
        self.element


    def act_event(self, event_action, element, *args, **kwargs):
        if event_action == self.FLOWTOHOST:
            element.send(args, kwargs)

        elif event_action == self.HOSTTOLINK:
            Host.Host.send(args, kwargs)

        elif event_action == self.LINKTRANSMIT:
            Link.Link.transmit(args, kwargs)

        elif event_action == self.LINKTOHOST:
            Link.Link.pick_pkg_from_buffer_out()
            Host.Host.receive(args, kwargs)

    def run
