#A MPI program that does the following for some arbitrary number of processes
#Author: Hongting Chen
#Pleas run with "mpiexec -n num_of_process python mpi_assignment_2.py "
import numpy
import sys
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

num = numpy.array(0)

if (rank!=0):
	comm.Recv(num, source=rank-1)
	print("Process", rank, "received the number", num, "from process", rank-1)
else:
	try:
		#Set the number's value if you are process 0
		a = int(input("please input your value (less than 100): "))
		num = numpy.array(a)
		#num = "s"
		#Process 0 reads a value from the user and 
		#verifies that it is an integer less than 100.
		if num < 100:
			print("Process", rank, "received the value", num, "from user")
		else: 
			print("Please input an value less than 100! ")
			sys.exit()
	except ValueError as e:
		print("Invalid Input")
		sys.exit()
	

if (rank != size-1):
	#process i sends the value to process i+1 which multiplies it by i+1
	comm.Send(num*(rank+1), dest = rank+1)
else:
	# Now process 0 can receive from the last process.
	comm.Send(num, dest = 0)

if (rank == 0):
	comm.Recv(num, size-1)
	print("Process", rank, "received the number", num, "from", size-1)
	

