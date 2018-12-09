import event_type
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

