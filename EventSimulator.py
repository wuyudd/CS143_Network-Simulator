from heapq import *
import EventAction

class EventSimulator(object):
    def __init__(self):
        self.events_queue = []


    def event_push(self, event):
        heappush(self.events_queue, event)

    def do_next_event(self):
        curr_event = heappop(self.events_queue)
        EventAction.EventAction.act_event(curr_event)

