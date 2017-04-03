
"""
    N-body simulation.
    Numba version
        Add @jit decorators to all funcitons
        Add function signatures to all funcitons
        Add a vectorized ufunc
    Runtime: 25.7323770523s
    R = L_opt / L_numba = 1.7
    So in my case using cython would speed up faster
"""

from itertools import combinations
from numba import jit, int32, float64, vectorize
import numpy as np


PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

BODIES = np.array([
    ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [SOLAR_MASS,0.0,0.0]),
    ([4.84143144246472090e+00,
                 -1.16032004402742839e+00,
                 -1.03622044471123109e-01],
                [1.66007664274403694e-03 * DAYS_PER_YEAR,
                 7.69901118419740425e-03 * DAYS_PER_YEAR,
                 -6.90460016972063023e-05 * DAYS_PER_YEAR],
                [9.54791938424326609e-04 * SOLAR_MASS,0.0,0.0]),
   ([8.34336671824457987e+00,
                4.12479856412430479e+00,
                -4.03523417114321381e-01],
               [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR],
               [2.85885980666130812e-04 * SOLAR_MASS,0.0,0.0]),
     ([1.28943695621391310e+01,
                -1.51111514016986312e+01,
                -2.23307578892655734e-01],
               [2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR],
               [4.36624404335156298e-05 * SOLAR_MASS,0.0,0.0]),
    ([1.53796971148509165e+01,
                 -2.59193146099879641e+01,
                 1.79258772950371181e-01],
                [2.68067772490389322e-03 * DAYS_PER_YEAR,
                 1.62824170038242295e-03 * DAYS_PER_YEAR,
                 -9.51592254519715870e-05 * DAYS_PER_YEAR],
                [5.15138902046611451e-05 * SOLAR_MASS,0.0,0.0])])

pairs = np.array(list(combinations(np.arange(BODIES.shape[0]), 2)))

@vectorize([float64(float64, float64)])
def vec_deltas(a, b):
    #Takes two NumPy arrays of floats and returns the difference between each element
    return a - b

@jit('void(int32, float64[:,:,:], float64)')
def advance(iterations, bodies = BODIES, dt = 0.01):
    '''
        advance the system one timestep
    '''

    for _ in range(iterations):

        for (body1, body2) in pairs:            
            x1 = bodies[body1, 0]
            v1 = bodies[body1, 1]
            m1 = bodies[body1, 2, 0]
            x2 = bodies[body2, 0]
            v2 = bodies[body2, 1]
            m2 = bodies[body2, 2, 0]
            dp = vec_deltas(x1, x2)
            mag = dt * (np.sum(dp**2) ** (-1.5))
            m1_mag = m1 * mag
            m2_mag = m2 * mag
            
            v1 -= dp * m2 * mag
            v2 += dp * m1 * mag

        for body in range(len(BODIES)):
            r = BODIES[body, 0]
            v = BODIES[body, 1]
            r += dt * v
            
@jit('float64(float64[:,:,:], float64)')       
def report_energy(bodies = BODIES, e=0.0):
    '''
        compute the energy and return it so that it can be printed
    '''
    for (body1, body2) in pairs:            
        x1 = bodies[body1, 0]
        v1 = bodies[body1, 1]
        m1 = bodies[body1, 2, 0]
        x2 = bodies[body2, 0]
        v2 = bodies[body2, 1]
        m2 = bodies[body2, 2, 0]
        dp = vec_deltas(x1, x2)
        mag = dt * (np.sum(dp**2) ** (-1.5))
        m1_mag = m1 * mag
        m2_mag = m2 * mag
            
        v1 -= dp * m2 * mag
        v2 += dp * m1 * mag
                
        
    for body in range(len(BODIES)):
        v = bodies[body, 1]
        m = bodies[body, 2, 0]
        
        e += m * np.sum(v**2) / 2.
        
    return e

@jit('void(int32, int32, int32)')
def nbody(loops, reference, iterations):

    
    '''
        nbody simulation
        loops - number of loops to run
        reference - body at center of system
        iterations - number of timesteps to advance
    '''

    # Set up global state
    # reference is the body in the center of the system
    # offset values from this reference

    p = np.zeros(3)
    for i in range(len(BODIES)):        
        v = BODIES[i, 1]
        m = BODIES[i, 2, 0]
        p -= v * m

    m = BODIES[reference, 2, 0]
    BODIES[reference, 1] = p / m


    for _ in range(loops):
        report_energy(BODIES)
        advance(iterations,BODIES)
        print(report_energy(BODIES))

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("nbody(100, 0, 20000)", setup = "from __main__ import nbody", number = 1))

