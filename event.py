"""
this class create a event type, specific information is in event_type.py file
all the classes in the event_type.py inherit from class Event.
"""


class Event(object):
    def __init__(self):
        self.start_time = 0.0

    def __lt__(self, other):
        return self.start_time < other.start_time

    def event_action(self):
        pass

    def set_start_time(self, time):
        self.start_time = time
        return

    def get_start_time(self):
        return self.start_time

