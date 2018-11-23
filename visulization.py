import matplotlib.pyplot as plt
from link import *
from router import *
from simulator import *

class Visulization(object):
    def __init__(self, links):
        self.links = links

    def plot_link_buffer_usage(self):

        # print("================================")
        # print(self.links['L1'].plot_link_buffer_time)
        # print(self.links['L1'].plot_link_buffer)

        plt.plot(self.links['L1'].plot_link_buffer_time, self.links['L1'].plot_link_buffer)

        plt.show()