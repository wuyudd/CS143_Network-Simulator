class Event(object):

    def __init__(self):
        self.start_time = 0.0

    def event_action(self):
        pass

    def set_start_time(self, time):
        self.start_time = time
        return

    def get_start_time(self):
        return self.start_time

