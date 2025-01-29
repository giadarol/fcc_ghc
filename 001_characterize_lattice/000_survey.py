import xtrack as xt
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('../fccee_z_strengths.py')

line = env['fccee_p_ring']

# Survey
sv = line.survey()
sv.plot()
