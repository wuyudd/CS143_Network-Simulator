from simulator import *
from visulization import *
import global_var

# link rate, link buffer usage, flow rate, flow window size, RTT

if __name__ == '__main__':
    sim = Simulator()
    sim_links, sim_flows = sim.run('test1.txt', 'flows1.txt')
    vis = Visulization(sim_links, sim_flows)
    #vis.plot_link_buffer_usage()
    vis.plot_window_size()
    vis.plot_rtt()


