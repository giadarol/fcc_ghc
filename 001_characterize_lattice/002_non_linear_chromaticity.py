import xtrack as xt
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

env = xt.Environment()
env.call('../fccee_t_lattice.py')
env.call('../fccee_t_strengths.py')

line = env['fccee_p_ring']

tw = line.twiss4d()

nlc = line.get_non_linear_chromaticity(delta0_range=(-0.005, 0.005),num_delta=20,
                                       fit_order=10)

# High order chromaticity values
print('\nHigh order chromaticity values:')
print(f"Q'x =    {nlc.dnqx[1]:.2e}")
print(f"Q''x =   {nlc.dnqx[2]:.2e}")
print(f"Q'''x =  {nlc.dnqx[3]:.2e}")
print(f"Q''''x = {nlc.dnqx[4]:.2e}")
print(f"Q'y =    {nlc.dnqy[1]:.2e}")
print(f"Q''y =   {nlc.dnqy[2]:.2e}")
print(f"Q'''y =  {nlc.dnqy[3]:.2e}")
print(f"Q''''y = {nlc.dnqy[4]:.2e}")

plt.figure(1)
plt.plot(nlc.delta0, nlc.qx - tw.qx, label=r'$\Delta Q_x$')
plt.plot(nlc.delta0, nlc.qy - tw.qy, label=r'$\Delta Q_y$')
plt.legend()
plt.xlabel(r'$\delta_0$')
plt.ylabel(r'$\Delta Q$')

plt.show()
