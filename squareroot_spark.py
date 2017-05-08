#program that calculate the average of the 
#square root of all the numbers from 1 to 1000
from pyspark import SparkContext
from operator import add
from math import sqrt

if __name__ == '__main__':

    sc = SparkContext("local", "squareroot_spark")
    # Create an RDD of numbers range from 1 to 1001
    nums = sc.parallelize(range(1,1001))
    # calculates the average of the square root of all the numbers
    squareroot = nums.map(sqrt)
    avg = squareroot.fold(0, add) / squareroot.count()
    print("The average of the square root of all numbers is ", avg)