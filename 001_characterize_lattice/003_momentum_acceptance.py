import xtrack as xt
import numpy as np

env = xt.Environment.from_json('../fccee_t_thick_thin.json.gz')

line = env.fccee_p_ring_thin

# For twiss 6d we set cavity lags to 180 degrees, as radiation is not active
line['lagca1'] = 0.5
line['lagca2'] = 0.5 # used only in fccee_t

# 6d twiss to check the optics
tw = line.twiss()

# Add toolkit to tha paths where python looks for modules
import sys
sys.path.append('../toolkit')

from momentum_acceptance import ActionMomentumAcceptance

nemitt_x = 6.33e-5
nemitt_y = 1.69e-7
energy_spread=3.9e-4
nn_y_r=15 # number of points 
max_y_r=15
global_xy_limit = 10e-2 # particles are lost when they reach this limit in x or y
num_turns = 100
act = ActionMomentumAcceptance(line,
            nemitt_x, nemitt_y, nn_y_r, max_y_r, energy_spread,
            global_xy_limit=global_xy_limit, num_turns=num_turns)

import matplotlib.pyplot as plt
plt.figure()
act.mom_acceptance(plot=True, with_progress=1)
plt.show()