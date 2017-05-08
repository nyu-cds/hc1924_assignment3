#program that calculates the product 
#of all the numbers from 1 to 1000 and prints the result
from pyspark import SparkContext
from operator import mul

if __name__ == '__main__':

    sc = SparkContext("local", "product_spark")
    # Create an RDD of numbers range from 1 to 1001
    nums = sc.parallelize(range(1,1001))
    # calculates the product of all the numbers
    print("The product of all numbers is ", nums.fold(1, mul))