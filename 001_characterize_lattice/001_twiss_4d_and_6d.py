import xtrack as xt
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('../fccee_z_strengths.py')

line = env['fccee_p_ring']

# For twiss 6d we set cavity lags to 180 degrees, as radiation is not active
line['lagca1'] = 0.5
line['lagca2'] = 0.5 # used only in fccee_t

# Twiss 4d
tw4d = line.twiss4d()

# Twiss 6d
tw6d = line.twiss()

# Show betas at IPs
print('\nMain optics functions at IPs:')
tw4d.cols['betx bety dx mux muy'].rows['ip.*'].show()

print('\nChromatic functions at IPs:')
tw4d.cols['wx_chrom wy_chrom'].rows['ip.*'].show()

print('\nTunes, chromaticities, coupling, momentum compaction factor:')
print(f'Qx = {tw4d.qx:.4f}')
print(f'Qy = {tw4d.qy:.4f}')
print(f'Qs = {tw6d.qs:.4f}')
print(f"Q'x = {tw4d.dqx:.2f}")
print(f"Q'y = {tw4d.dqy:.2f}")
print(f'|C-| = {tw4d.c_minus:.3e}')
print(f'mom_compaction = {tw4d.momentum_compaction_factor:.3e}')

# plot 4d twiss (full)
tw4d.plot()

# plot chromatic functions and second order dispersion
pp = tw4d.plot(yl='wx_chrom wy_chrom', yr='ddx')
pp.ylim(left_lo=0, left_hi=10_000, right_lo=-200)
pp.xlim(30_000, 60_000)

plt.show()
