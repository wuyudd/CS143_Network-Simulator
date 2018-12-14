"""
main.py has the main function for running and visualizing.
"""
from visualization import *
from optparse import OptionParser


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--filetxt", dest="filename_test", help="Test case txt filename e.g. test2.txt")
    parser.add_option("-f", "--fileflow", dest="filename_flow", help="flows txt filename e.g. flows2.txt")
    options, _ = parser.parse_args()
    sim = Simulator(vars(options))
    # read in the test case file to build graph and read the flows, return the links and flows.
    # sim_links, sim_flows = sim.run('test2.txt', 'flows2.txt')
    # read in the test case file and the corresponding links and flows and visualize the measuring metrics.
    # vis = Visualization(sim_links, sim_flows, 'test2.txt')
    sim_links, sim_flows = sim.run()
    vis = Visualization(sim_links, sim_flows, vars(options))
    vis.plot_link_buffer_usage()
    vis.plot_link_rate()
    vis.plot_flow_rate()
    vis.plot_window_size()
    # vis.plot_part_window_size()
    vis.plot_rtt()






