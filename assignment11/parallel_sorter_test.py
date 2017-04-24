'''
Easy test for Collective Communication Assignment
Author:Hongting Chen
04/22/2017

Please run with "python parallel_sorter_test.py"

'''
import parallel_sorter
import numpy as np

sorted_n = parallel_sorter.parallel_sort()
final_n = np.concatenate(sorted_n)

assert all(final_n[i] <= final_n[i+1] for i in range(len(final_n)-1))
print("The final array is in ascending order. The parallel_sort() function works!")
