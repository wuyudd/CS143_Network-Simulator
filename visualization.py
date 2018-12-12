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
        self.color = ["#DB7093", "#4682B4", "#32CD32"]

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
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, color=self.color[0], label=link_id)
                if link_id == 'L2':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, color=self.color[1], label=link_id)
                if link_id == 'L3':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, color=self.color[2], label=link_id)
        elif self.graph_file_name == 'extra_test.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L2':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, color=self.color[1], label=link_id)
                if link_id == 'L4':
                    plt.scatter(link.plot_link_buffer_time, link.plot_link_buffer, s=self.point_size, color=self.color[2], label=link_id)
        plt.legend(fontsize=24, loc=1)
        plt.xlabel('time/s', fontsize=24)
        plt.ylabel('link_buffer_usage/KB', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.savefig('result_figures/' + self.graph_file_name.split('.')[0] + '_link_buffer_usage.png')
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
                i = int(link_id[1])-1
                if link_id == 'L1':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, color=self.color[i], label=link_id)
                if link_id == 'L2':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, color=self.color[i], label=link_id)
                if link_id == 'L3':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, color=self.color[i], label=link_id)
        elif self.graph_file_name == 'extra_test.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L2':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, color=self.color[1], label=link_id)
                if link_id == 'L4':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, color=self.color[2], label=link_id)
        else:
            print("No such test case file found!")
        plt.legend(fontsize=24, loc=1)
        plt.xlabel('time/s', fontsize=24)
        plt.ylabel('link_rate/Mbps', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.savefig('result_figures/' + self.graph_file_name.split('.')[0] + '_link_rate.png')
        plt.show()

    def plot_flow_rate(self):
        if self.graph_file_name == 'test0.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L1':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, label='F1')
        elif self.graph_file_name == 'test1.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L0':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, label='F1')
        elif self.graph_file_name == 'test2.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L4':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, c=self.color[0], label='F1')
                if link_id == 'L0':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, c=self.color[1], label='F2')
                if link_id == 'L6':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, c=self.color[2], label='F3')
        elif self.graph_file_name == 'extra_test.txt':
            plt.figure(figsize=(30, 8))
            for link_id, link in self.links.items():
                if link_id == 'L1':
                    plt.scatter(global_var.plot_link_rate_time_axis, link.plot_link_rate, s=self.point_size, c=self.color[0], label='F1')
        else:
            print("No such test case file found!")
        plt.legend(fontsize=24, loc=1)
        plt.xlabel("time/s", fontsize=24)
        plt.ylabel('flow_rate/Mbps', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.savefig('result_figures/' + self.graph_file_name.split('.')[0] + '_flow_rate.png')
        plt.show()

    def plot_window_size(self):
        plt.figure(figsize=(30, 8))
        for flow_id, flow in self.flows.items():
            i = int(flow_id[1])-1
            plt.scatter(flow.plot_window_size_timestamp, flow.plot_window_size, s=self.point_size, color=self.color[i], label=flow_id)
        plt.legend(fontsize=24, loc=1)
        plt.xlabel("time/s", fontsize=24)
        plt.ylabel('window_size/pkts', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.savefig('result_figures/' + self.graph_file_name.split('.')[0] + '_window_size.png')
        plt.show()

    def plot_part_window_size(self):
        plt.figure(figsize=(30, 8))
        for flow_id, flow in self.flows.items():
            i = int(flow_id[1]) - 1
            plt.scatter(flow.plot_window_size_timestamp, flow.plot_window_size, s=self.point_size, color=self.color[i], label=flow_id)
        plt.legend(fontsize=24, loc=1)
        plt.xlabel("time/s", fontsize=24)
        plt.ylabel('window_size/pkts', fontsize=24)
        plt.xlim(0, 30)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.savefig('result_figures/' + self.graph_file_name.split('.')[0] + 'clear_window_size_reno.png')
        plt.show()

    def plot_rtt(self):
        plt.figure(figsize=(30, 8))
        for flow_id, flow in self.flows.items():
            i = int(flow_id[1]) - 1
            plt.scatter(flow.plot_window_size_timestamp, flow.plot_rtt, s=self.point_size, color=self.color[i], label=flow_id)
        plt.legend(fontsize=24, loc=1)
        plt.xlabel('time/s', fontsize=24)
        plt.ylabel('RTT/s', fontsize=24)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.savefig('result_figures/' + self.graph_file_name.split('.')[0] + '_rtt.png')
        plt.show()



