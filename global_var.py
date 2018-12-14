"""
gloabl_var.py maintains the global variables needed.
"""
queue = [] # queue is a priority queue to store the event
timestamp = float(0.0) # timestamp is a timer globally
# period is used for update the routing information
# in each period, each router will only accept the routing information sent from other routers in current period
period = 0
# updating_flag is a boolean
# when it is True: each router has the authorization to receive the information from other routers
# when it is False: each router has NO authorization to receive the information from other routers
updating_flag = False

# following global variable is for plotting
plot_link_rate_time_axis = []
plot_window_size_pkt_timestamp = []