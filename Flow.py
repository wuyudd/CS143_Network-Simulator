class Flow(object):
    def __init__(self, id, src, dest, data_amount, start):
        self.id = id
        self.src = src
        self.dest = dest
        self.data_amount = data_amount * 1000
        self.start = start


