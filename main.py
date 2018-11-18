import Host
import Link
import EventSimulator
import EventAction

if __name__ == '__main__':
    link = Link.Link()
    host_a = Host.Host("1.1.1.1", link)
    host_b = Host.Host("2.2.2.2", link)
    event = EventAction.EventAction.HOSTTOLINK
    event_sim = EventSimulator.EventSimulator()

    # 要对event_sim里的queue不断地push input file里面的所有events
    # 调用event_sim的push函数
    event_sim.event_push(event)

    while not event_sim.events_queue:
        event_sim.do_next_event()




