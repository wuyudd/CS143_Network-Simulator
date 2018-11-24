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
        plt.subplot(611)
        plt.scatter(self.links['L0'].plot_link_buffer_time, self.links['L0'].plot_link_buffer, s = 3)
        plt.subplot(612)
        plt.scatter(self.links['L1'].plot_link_buffer_time, self.links['L1'].plot_link_buffer, s=3)
        plt.subplot(613)
        plt.scatter(self.links['L2'].plot_link_buffer_time, self.links['L2'].plot_link_buffer, s=3)
        plt.subplot(614)
        plt.scatter(self.links['L3'].plot_link_buffer_time, self.links['L3'].plot_link_buffer, s=3)
        plt.subplot(615)
        plt.scatter(self.links['L4'].plot_link_buffer_time, self.links['L4'].plot_link_buffer, s=3)
        plt.subplot(616)
        plt.scatter(self.links['L5'].plot_link_buffer_time, self.links['L5'].plot_link_buffer, s=3)

        plt.show()

        plt.subplot(611)
        plt.plot(global_var.plot_link_rate_time_axis, self.links['L0'].plot_link_rate)
        plt.subplot(612)
        plt.plot(global_var.plot_link_rate_time_axis, self.links['L1'].plot_link_rate)
        plt.subplot(613)
        plt.plot(global_var.plot_link_rate_time_axis, self.links['L2'].plot_link_rate)
        plt.subplot(614)
        plt.plot(global_var.plot_link_rate_time_axis, self.links['L3'].plot_link_rate)
        plt.subplot(615)
        plt.plot(global_var.plot_link_rate_time_axis, self.links['L4'].plot_link_rate)
        plt.subplot(616)
        plt.plot(global_var.plot_link_rate_time_axis, self.links['L5'].plot_link_rate)


        plt.show()