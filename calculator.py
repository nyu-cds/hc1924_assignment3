"""
Original Runtime: 2.23 s
Improved Runtime: 9.37 ms
Speedup: 238

If the colleage have a good understanding of numpy, he should be familar with numpy's builtin function np.hypot()
and use this function to do calculation instead of writing the break-down steps. np.hypot() returns 
sqrt(x**2 + y**2) for two arrays, a and b, element-wise. 

Below are part of the function test report with line_profile.

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    40                                           def hypotenuse(x,y):
    45         1      1061781 1061781.0     26.0      xx = multiply(x,x)
    46         1      1032920 1032920.0     25.3      yy = multiply(y,y)
    47         1      1089490 1089490.0     26.7      zz = add(xx, yy)
    48         1       902316 902316.0     22.1      return sqrt(zz)

     1                                           def add(x,y):
     6         1            4      4.0      0.0      m,n = x.shape
     7         1         2048   2048.0      0.1      z = np.zeros((m,n))
     8      1001          589      0.6      0.0      for i in range(m):
     9   1001000       483601      0.5     28.7          for j in range(n):
    10   1000000      1200413      1.2     71.2              z[i,j] = x[i,j] + y[i,j]
    11         1            1      1.0      0.0      return z


    14                                           def multiply(x,y):
    19         2            7      3.5      0.0      m,n = x.shape
    20         2         4366   2183.0      0.1      z = np.zeros((m,n))
    21      2002         1132      0.6      0.0      for i in range(m):
    22   2002000       964872      0.5     28.7          for j in range(n):
    23   2000000      2386601      1.2     71.1              z[i,j] = x[i,j] * y[i,j]
    24         2            2      1.0      0.0      return z

    27                                           def sqrt(x):
    31         1           13     13.0      0.0      from math import sqrt
    32         1            3      3.0      0.0      m,n = x.shape
    33         1         4764   4764.0      0.3      z = np.zeros((m,n))
    34      1001          641      0.6      0.0      for i in range(m):
    35   1001000       537061      0.5     34.0          for j in range(n):
    36   1000000      1038325      1.0     65.7              z[i,j] = sqrt(x[i,j])
    37         1            1      1.0      0.0      return z
"""

if __name__ == '__main__':
    import numpy as np
    M = 10**3
    N = 10**3

    A = np.random.random((M,N))
    B = np.random.random((M,N))

    print(np.hypot(A,B))

