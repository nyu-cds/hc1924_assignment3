# This function prints all binary strings of 
# length n that contain k zero bits
# 
# Run as python binary.py n k

import sys
from itertools import permutations
from itertools import repeat

def zbits(n, k):
    #create the iterator that generate certain numbers of ones and zeros 
    iterator1 = repeat('1', n-k)
    iterator0 = repeat('0', k)
    
    #generate a string of certain ones and zeros
    element = []
    for val in iterator1:
        element.append(val)
    for val in iterator0:
        element.append(val)
        
    string = ''.join(element)
    slist = set()
    
    #create the iterator that generates combinations of ceratin ones and zeros
    for item in permutations(string, n):
        slist.add(''.join(item))
    
    print(slist)
    
   
if __name__ == '__main__':
    
    #import binary
    #assert binary.zbits(4, 3) == zbits(4, 3)
    #assert binary.zbits(4, 1) == zbits(4, 1)
    #assert binary.zbits(5, 4) == zbits(5, 4)

    # this line checks how many arguments are passed to python
    if not len(sys.argv) == 3:
        print("Invalid number of arguments. Run as python binary.py n k")
        sys.exit()
        
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    print(zbits(n,k))