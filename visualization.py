"""
visualization.py is used for visualizing the measuring metrics.
Supported plotting:
    link buffer usage (KB)
    link rate         (Mbps)
    flow rate         (Mbps)
    window size       (pkts)
    RTT               (s)
"""
import matplotlib.pyplot as plt
from simulator import *


class Visualization(object):
    def __init__(self, links, flows, graph_file_name):
        self.links = links
        self.flows = flows
        self.graph_file_name = graph_file_name
        self.point_size = 20

    def plot_link_buffer_usage(self):
        if self.graph_file_name == 'test0.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L1':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label=link_id)
        elif self.graph_file_name == 'test1.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L1':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label=link_id)
                if link_id == 'L2':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label=link_id)
        elif self.graph_file_name == 'test2.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L1':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label=link_id)
                if link_id == 'L2':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label=link_id)
                if link_id == 'L3':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label=link_id)
        plt.legend(fontsize=24)
        plt.xlabel('time/s', fontsize=24)
        plt.ylabel('link_buffer_usgae/KB', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.show()

    def plot_link_rate(self):
        if self.graph_file_name == 'test0.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L1':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, label=link_id)
        elif self.graph_file_name == 'test1.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L1':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, label=link_id)
                if link_id == 'L2':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, label=link_id)
        elif self.graph_file_name == 'test2.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L1':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, label=link_id)
                if link_id == 'L2':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, label=link_id)
                if link_id == 'L3':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, label=link_id)
        else:
            print("No such test case file found!")
        plt.legend(fontsize=24)
        plt.xlabel('time/s', fontsize=24)
        plt.ylabel('link_rate/Mbps', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.show()

    def plot_flow_rate(self):
        if self.graph_file_name == 'test0.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L1':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label='flow_1')
        elif self.graph_file_name == 'test1.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L0':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label='flow_1')
        elif self.graph_file_name == 'test2.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L4':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label='flow_1')
                if link_id == 'L0':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label='flow_2')
                if link_id == 'L6':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, label='flow_3')
        else:
            print("No such test case file found!")
        plt.legend(fontsize=24)
        plt.xlabel("time/s", fontsize=24)
        plt.ylabel('flow_rate/Mbps', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.show()

    def plot_window_size(self):
        plt.figure(figsize=(30, 8))
        for flow_id, flow in self.flows.items():
            plt.scatter(flow.plot_window_size_timestamp, flow.plot_window_size, s=self.point_size, label=flow_id)
        plt.legend(fontsize=24)
        plt.xlabel("time/s", fontsize=24)
        plt.ylabel('window_size/pkts', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.show()

    def plot_rtt(self):
        plt.figure(figsize=(30, 8))
        for flow_id, flow in self.flows.items():
            plt.scatter(flow.plot_window_size_timestamp, flow.plot_rtt, s=self.point_size, label=flow_id)
        plt.legend(fontsize=24)
        plt.xlabel('time/s', fontsize=24)
        plt.ylabel('RTT/s', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.show()



