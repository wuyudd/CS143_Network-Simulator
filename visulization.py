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

        plt.figure(figsize=(16, 16))
        plt.suptitle('link buffer usage', fontsize=12)

        plt.subplot(611)
        plt.plot(self.links['L0'].plot_link_buffer_time, self.links['L0'].plot_link_buffer)
        plt.xlabel('time(s)')
        plt.ylabel('L0_Buffer')

        plt.subplot(612)
        plt.scatter(self.links['L1'].plot_link_buffer_time, self.links['L1'].plot_link_buffer, s=3)
        plt.xlabel('time(s)')
        plt.ylabel('L1_Buffer')
        # delete it
        '''
        plt.subplot(613)
        plt.scatter(self.links['L1*'].plot_link_buffer_time, self.links['L1*'].plot_link_buffer, s=3)
        plt.xlabel('time(s)')
        plt.ylabel('L1*_Buffer')
        '''
        plt.subplot(613)
        plt.scatter(self.links['L2'].plot_link_buffer_time, self.links['L2'].plot_link_buffer, s=3)
        plt.xlabel('time(s)')
        plt.ylabel('L2_Buffer')
        plt.subplot(614)
        plt.scatter(self.links['L3'].plot_link_buffer_time, self.links['L3'].plot_link_buffer, s=3)
        plt.xlabel('time(s)')
        plt.ylabel('L3_Buffer')
        plt.subplot(615)
        plt.scatter(self.links['L4'].plot_link_buffer_time, self.links['L4'].plot_link_buffer, s=3)
        plt.xlabel('time(s)')
        plt.ylabel('L4_Buffer')
        plt.subplot(616)
        plt.scatter(self.links['L5'].plot_link_buffer_time, self.links['L5'].plot_link_buffer, s=3)
        plt.xlabel('time(s)')
        plt.ylabel('L5_Buffer')

        plt.figure(figsize=(16, 16))
        #plt.suptitle('link rate', fontsize=12)
        #plt.subplot(611)


        plt.subplot(611)
        plt.scatter(global_var.plot_link_rate_time_axis, self.links['L0'].plot_link_rate, s=3)
        plt.xlabel('time(s)')
        plt.ylabel('L0')

        plt.subplot(612)
        plt.scatter(global_var.plot_link_rate_time_axis, self.links['L1'].plot_link_rate, s=3)
        plt.xlabel('time(s)')
        plt.ylabel('L1')
        # delete it
        '''
        plt.subplot(613)
        plt.scatter(global_var.plot_link_rate_time_axis, self.links['L1*'].plot_link_rate, s=3)
        plt.xlabel('time(s)')
        plt.ylabel('L1*')
        '''
        plt.subplot(613)
        plt.scatter(global_var.plot_link_rate_time_axis, self.links['L2'].plot_link_rate, s = 3)
        plt.xlabel('time(s)')
        plt.ylabel('L2')
        plt.subplot(614)
        plt.scatter(global_var.plot_link_rate_time_axis, self.links['L3'].plot_link_rate, s = 3)
        plt.xlabel('time(s)')
        plt.ylabel('L3')
        plt.subplot(615)
        plt.scatter(global_var.plot_link_rate_time_axis, self.links['L4'].plot_link_rate, s = 3)
        plt.xlabel('time(s)')
        plt.ylabel('L4')
        plt.subplot(616)
        plt.scatter(global_var.plot_link_rate_time_axis, self.links['L5'].plot_link_rate, s = 3)
        plt.xlabel('time(s)')
        plt.ylabel('L5')

        plt.show()


