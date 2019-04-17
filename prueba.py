# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:06:12 2019

@author: Bielo
"""

'''
def delete_first_line():
    with open("file.txt", "r") as f:
        lines = f.readlines()
    
    print(range(1,len(lines)))
    
    count =range(1,len(lines))
    
    with open("file.txt", "w") as f:
        for i in  count:
        #for line in lines:
        #    if line.strip("\n") != "nickname_to_delete":
        #        f.write(line)
            f.write(lines[i])
    
    
    
delete_first_line()
'''

count = range(1,100)

for x in count:
    print(x)