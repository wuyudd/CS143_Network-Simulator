# CS143_Network-Simulator
Course project of CS143_Network-Simulator, Caltech, 2018
Group member: Wen Gu, Sha Sha, Feng Jiang, Yu Wu

Here is about the whole process of our group project for CS143 Network-Simulator Course Project.
Description from offcial guidelines (http://courses.cms.caltech.edu/cs143/Project/guidelines.pdf)
Test cases from official websites (http://courses.cms.caltech.edu/cs143/Project/test_cases.pdf)

How to run our codes:
  Just run main.py
Done! :)

If you want to change the test case, just change the 'testi.txt' and 'flowsi.txt' in the main.py line 9 and line 10.
i.e., 
for test case 0: 
  sim_links, sim_flows = sim.run('test0.txt', 'flows1.txt')
  vis = Visualization(sim_links, sim_flows, 'test0.txt')
for test case 1: 
  sim_links, sim_flows = sim.run('test1.txt', 'flows1.txt')
  vis = Visualization(sim_links, sim_flows, 'test1.txt')
for test case 2: 
  sim_links, sim_flows = sim.run('test2.txt', 'flows2.txt')
  vis = Visualization(sim_links, sim_flows, 'test2.txt')

# End of README.md
