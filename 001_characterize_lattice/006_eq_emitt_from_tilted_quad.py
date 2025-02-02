import xtrack as xt
import xobjects as xo
import numpy as np

env = xt.Environment.from_json('../fccee_z_thick_thin.json.gz')
n_turns_track_test = 6000

# env = xt.Environment.from_json('../fccee_t_thick_thin.json.gz')
# n_turns_track_test = 1000

line = env.fccee_p_ring_thin

# For twiss 6d we set cavity lags to 180 degrees, tapering will adjust the phase
line['lagca1'] = 0.5
line['lagca2'] = 0.5 # used only in fccee_t


num_particles_test = 150

line.replace_all_repeated_elements()

line['qc1r1.2'].rot_s_rad = 0.5e-5
line['qc1l1.1'].rot_s_rad = 0.1e-5
tw0 = line.twiss4d()

line.configure_radiation(model='mean')
line.compensate_radiation_energy_loss()
tw = line.twiss(eneloss_and_damping=True)

bsize = tw.get_beam_covariance(
    gemitt_x=tw.eq_gemitt_x,
    gemitt_y=tw.eq_gemitt_y,
    gemitt_zeta=tw.eq_gemitt_zeta)

bsize_v_emit_only = tw.get_beam_covariance(
    gemitt_x=0.,
    gemitt_y=tw.eq_gemitt_y,
    gemitt_zeta=0.)

bsize_disp_only = tw.get_beam_covariance(
    gemitt_x=0.,
    gemitt_y=0.,
    gemitt_zeta=tw.eq_gemitt_zeta)

print('Vertical beam size:           ', bsize['sigma_y', 'ip.1'])
print('Vertical beam size (emit only): ', bsize_v_emit_only['sigma_y', 'ip.1'])

line.configure_radiation(model='quantum')
p = line.build_particles(num_particles=num_particles_test)

# Switch to multithreaded
line.discard_tracker()
line.build_tracker(_context=xo.ContextCpu(omp_num_threads='auto'),
                   use_prebuilt_kernels=False)

line.track(p, num_turns=n_turns_track_test, turn_by_turn_monitor=True, time=True,
           with_progress=10)
mon_at_start = line.record_last_track
print(f'Tracking time: {line.time_last_track}')

# Plots
import matplotlib.pyplot as plt
plt.close('all')

line.configure_radiation(model='mean') # Leave the line in a twissable state
mon = line.record_last_track

fig = plt.figure(figsize=(6.4, 4.8*1.3))

spx = fig. add_subplot(3, 1, 1)
spx.plot(1e6 * np.std(mon.x, axis=0), label='track')
spx.axhline(1e6 * bsize['sigma_x', 'ip.1'], color='red', label='twiss')
spx.legend(loc='lower right', fontsize='small')
spx.set_ylabel(r'$\sigma_{x}$ [$\mu m$]')
spx.set_ylim(bottom=0)

spy = fig. add_subplot(3, 1, 2, sharex=spx)
spy.plot(1e9 * np.std(mon.y, axis=0), label='track')
spy.axhline(1e9 * bsize['sigma_y', 'ip.1'], color='red', label='twiss')
spy.set_ylabel(r'$\sigma_{y}$ [nm]')
spy.set_ylim(bottom=0)

spz = fig. add_subplot(3, 1, 3, sharex=spx)
spz.plot(np.std(1e3*mon.zeta, axis=0))
spz.axhline(1e3*bsize['sigma_zeta', 'ip.1'], color='red', label='twiss')
spz.set_ylabel(r'$\sigma_{z}$ [mm]')
spz.set_ylim(bottom=0)
spz.set_xlabel('s [m]')
plt.subplots_adjust(left=.2, top=.95, hspace=.2)

plt.show()