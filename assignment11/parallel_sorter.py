'''
Collective Communication Assignment
Author:Hongting Chen
04/22/2017

This program takes in a number "a" of buffer, the root process 
generates "a" of unsorted integers.Then slice it into bins by value 
and send each bin to the other processes to sort. The sorted data 
should then be sent back to the root process and put into rank order.
#Pleas run with "mpiexec -n _you_num_ python parallel_sorted.py "

'''

import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def parallel_sort():
	if rank == 0:
		try:
			#generete random integers
			a = int(input("please input your buffer size: "))
			n = np.random.randint(0,a+1,a)
			# divide the data into bins, one for each process rank
			freq, bins = np.histogram(n, bins = size) 
			# find the index in the bins of each element
			pos = np.digitize(n, bins) 
			np.place(pos, pos==size+1, size) # since the bins are half open
		except ValueError as e:
			print("Invalid input")
			comm.Abort()

		process = [[] for i in range(size)]
		for i in range(len(n)):
			for j in range(size):
				if pos[i] == (j+1):
					process[j].append(n[i])
	else:
		n = None
		process = None

	# scatter bins to all processes
	local_n = comm.scatter(process,root = 0)

	# innner sorting
	local_n.sort()

	# sending sorted bins back to root master
	sorted_n = comm.gather(local_n,root = 0)
	# print out the sorted array of numbers
	return sorted_n

if __name__ == '__main__':
	sorted_n = parallel_sort()
	if rank ==0:
		final_n = np.concatenate(sorted_n)
		print("Sorted array:\n",final_n)
