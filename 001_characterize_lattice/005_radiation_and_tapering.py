import matplotlib.pyplot as plt

import xtrack as xt

env = xt.Environment()

# Z configuration
# env.call('../fccee_z_lattice.py')
# env.call('../fccee_z_strengths.py')
# env.call('../toolkit/install_rf_cavities_rpo.py') # Install realistic rf cavities
# env['l400_2'] = 0.5 # For twiss 6d we set cavity lags to 180 degrees, tapering will adjust the phase

# t configuration
env.call('../fccee_t_lattice.py')
env.call('../fccee_t_strengths.py')
env['lagca1'] = 0.5
env['lagca2'] = 0.5

# Get thin line
line = env.fccee_p_ring

tt = line.get_table()
tt_cav = tt.rows[tt.element_type == 'Cavity']

tw0 = line.twiss4d()

line.configure_radiation(model='mean')
line.compensate_radiation_energy_loss()

tw = line.twiss(eneloss_and_damping=True, delta_chrom=1e-12)

plt.close('all')
tw.plot('delta', lattice=False)
plt.show()
