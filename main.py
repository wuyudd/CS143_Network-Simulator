from simulator import *
from visulization import *
import global_var

# link rate, link buffer usage, flow rate, flow window size, RTT

if __name__ == '__main__':
    sim = Simulator()
    sim_links = sim.run()

    vis = Visulization(sim_links)
    vis.plot_link_buffer_usage()



