"""
Using fem1d.py to solve an Euler Bernoulli beam problem
"""
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from fem1d import EulerBernoulliBeam
def f(x):
    if(x >=0 and x <= 1):
        return 8000 - 8000*x
    if(x>= 2 and x<= 4):
        return 8000
    return 0

EI = 10000000
b = lambda x: EI
beam = EulerBernoulliBeam(6, 6, f=f, b=b, title='Euler Bernoulli Beam, 6 elements')
beam.add_boundary_condition(0, loc='l', var_type='primary', dof=1)
beam.add_boundary_condition(0, loc='l', var_type='primary', dof=2)
beam.add_boundary_condition(0, loc='r', var_type='primary', dof=1)
beam.add_boundary_condition(0, loc='r', var_type='primary', dof=2)
beam.build_cards()
beam.save_card('beamcard.inp')
sol = beam.run()
print(beam.card)
sleep(5)
beam.plot_beam()