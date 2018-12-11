from simulator import *
from visualization import *
import global_var

# link rate, link buffer usage, flow rate, flow window size, RTT

if __name__ == '__main__':
    sim = Simulator()
    sim_links, sim_flows = sim.run('test2.txt', 'flows2.txt')
    vis = Visualization(sim_links, sim_flows, 'test2.txt')
    vis.plot_link_buffer_usage()
    vis.plot_link_rate()
    vis.plot_window_size()
    vis.plot_rtt()
    vis.plot_flow_rate()


