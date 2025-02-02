import matplotlib.pyplot as plt

import xtrack as xt

env = xt.Environment.from_json('../fccee_z_thick_thin.json.gz')

# Istall relalistic rf cavities
env.call('../toolkit/install_rf_cavities_rpo.py')

line = env.fccee_p_ring_thin

# For twiss 6d we set cavity lags to 180 degrees, tapering will adjust the phase
line['l400_2'] = 0.5

tt = line.get_table()
tt_cav = tt.rows[tt.element_type == 'Cavity']

tw0 = line.twiss4d()

line.configure_radiation(model='mean')
line.compensate_radiation_energy_loss()
tw = line.twiss(eneloss_and_damping=True)

plt.close('all')
tw.plot('delta')
plt.show()
