#MPI program in which the processes with even rank print “Hello” 
#and the processes with odd rank print “Goodbye”
from mpi4py import MPI

#MPI.COMM_WORLD is communicator. 
#In mpi4py, communicators are represented by the Comm class.
comm = MPI.COMM_WORLD
#Get_rank() returns the rank of the calling process within the communicator.
rank = comm.Get_rank()
#Get_size() returns the total number of processes contained in the communicator
#size = comm.Get_size()

if (rank % 2) == 0:
    print("Hello from process %d" % (rank))
else:
    print("Goodbye from process %d" % (rank))