"""
global_consts.py maintains the global constants needed.
"""
# specifies the size for each class of packets
# the size is in byte
PACKETSIZE = float(1024)
ACKSIZE = float(64)
# specifies the 2 second duration for router to communicate with other to exchange the routing information
# specificly, exchange the information of the weight for each link
UPDATEDURATION = float(2)
# update the routing table every 5 second
UPDATEFREQUENCY = float(5)

# specifies the frequency for reading link rate
READLINKRATEFREQUENCY = float(0.05)
# used for calculate the weight of each link
WEIGHTFACTOR = float(10)