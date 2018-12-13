"""
main.py has the main function for running and visualizing.
"""
from visualization import *

if __name__ == '__main__':
    sim = Simulator()
    # read in the test case file to build graph and read the flows, return the links and flows.
    sim_links, sim_flows = sim.run('test5.txt', 'flows5.txt')
    # read in the test case file and the corresponding links and flows and visualize the measuring metrics.
    vis = Visualization(sim_links, sim_flows, 'test5.txt')
    vis.plot_link_buffer_usage()
    vis.plot_link_rate()
    vis.plot_flow_rate()
    vis.plot_window_size()
    vis.plot_part_window_size()
    vis.plot_rtt()



