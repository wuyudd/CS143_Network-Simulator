# CS143_Network-Simulator
Course project of CS143_Network-Simulator, Caltech, 2018 Fall.  

Group member: Wen Gu, Feng Jiang, Sha Sha, Yu Wu.

Here is about the whole process of our group project for CS143 Network-Simulator Course Project.  

Description from offcial guidelines (http://courses.cms.caltech.edu/cs143/Project/guidelines.pdf).  

Test cases from official websites (http://courses.cms.caltech.edu/cs143/Project/test_cases.pdf; https://d1b10bmlvqabco.cloudfront.net/attach/jmwaxhnfqdm6hk/i0ogs5hbbrrhs/jpda7f6zzvi9/new_test_case.pdf).  

Environment:  

    Python 3.7
  
How to run our codes:  

Type in the following in the terminal:  
(under the directory of CS143_Network-Simulator; -t to choose the testX.txt, -f to choose the corresponding flowsX.txt; package matplotlib needed for plotting: pip install matplotlib)  

e.g.  
  
    python ./main.py -t test2.txt -f flows2.txt  
    
If you want to choose TCP algorithms, please modify the rightmost column of the flowsX.txt.  

e.g.   

    F1	H1	H2	20971520	1.0	FAST  
  
# End of README.md
