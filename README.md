# CS143_Network-Simulator
Course project of CS143_Network-Simulator

Here is about the whole process of our group project for CS143 Network-Simulator Course Project.
Description from offcial guidelines (http://courses.cms.caltech.edu/cs143/Project/guidelines.pdf):

To do: 
• Write a program that can take a description of an abstract network and simulate its operation.

Purpose: 
• To create a tool with which theoretical analyses of networks can be validated
• To help you gain a greater understanding of some of the common components and mechanics underlying today’s networked world.

High-level Overview:
• Take as input a description of a network in a format of your choice.
• Run a simulation of the described network for a user-specified duration.
• Record data from user-specified simulation variables at regular intervals.
• Output graphs after each run showing the progression of the specified variables over time.

Core Parts:
• Components: hosts, routers, flows, and links. 
  • Hosts: individual endpoint computers; 
  • Routers: the network equipment that sits between hosts;
    (1)Property: Every host and router has a network address. This address uniquely identifies each node on the network. Hosts    will have at most one link connected; routers may have an arbitrary number. Routers will implement a dynamic routing protocol that uses "link cost" as a distance metric and route packets along "a shortest path" according to this metric. (routers - link cost as distance metric - shortest path)
    (2)Assumption: Every host and router can process an infinite amount of incoming data instantaneously
  • Links: communication lines that connect hosts and routers together;
    (1)Property: Links connect hosts and routers, and carry packets from one end to the other. Every link has a specified capacity.
    (2)Assumption: Link buffers are "FIFO". All links are "full-duplex". Each link will have a "static cost", based on some intrinsic property of the link (e.g. its ‘length’). Additionally, the link should also be able to take a "dynamic cost dependent on link congestion". (link cost = static cost + dynamic cost dependent on link congestion)
  • Flows: active connections; 
    (1)Property: Flows have a source and destination address, and generate packets at a rate controlled by the congestion control algorithm defined for that flow. (flow rate controlled by congestion control algorithm)
    
    data packets: a fixed size of 1024 bytes
    acknowledgement packets: a fixed size of 64 bytes
    Link buffer size, capacity, and propagation delay must be user-specifiable, as must flow data size and start time.
    
• Congestion Control Algorithm: TCP Reno and FAST-TCP
  • Be able to choose independently between them for each flow. Flows may send a continuous stream of data, or may send a finite user-specifiable amount of data; they may also start immediately or after some user-specifiable delay.

Measuring:
• Per-link buffer occupancy, packet loss, and flow rate. 
• Per-flow send/receive rate and packet round-trip delay. 
• Per-host send/receive rate.



