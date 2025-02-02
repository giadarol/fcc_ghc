import xtrack as xt
import numpy as np

env = xt.Environment()

# lattice_config= 'z'
lattice_config = 't'

env.call(f'../fccee_{lattice_config}_lattice.py')
env.call(f'../fccee_{lattice_config}_strengths.py')

line_thick = env.fccee_p_ring
tw_thick = line_thick.twiss4d(strengths=True)

# Sort quads by beta function
tw_quads = tw_thick.rows[tw_thick.element_type == 'Quadrupole']
bet_max_xy = [(max([tw_quads.betx[ii], tw_quads.bety[ii]]))
              for ii in range(len(tw_quads))]
tw_quads['bet_max_xy'] = np.array(bet_max_xy)
i_sorted = np.argsort(bet_max_xy)
tw_quads_sorted = tw_quads.rows[i_sorted[::-1]]

line = line_thick.copy(shallow=True)

# Remove repeated elements to be ready to install magnetic errors and misalignments
line.replace_all_repeated_elements()

Strategy = xt.slicing.Strategy
Teapot = xt.slicing.Teapot

if lattice_config == 'z':
    n_slice_arc_quad = 10
elif lattice_config == 't':
    n_slice_arc_quad = 15
else:
    raise ValueError(f'Unknown lattice configuration: {lattice_config}')

slicing_strategies = [
    Strategy(slicing=None),  # Default catch-all as in MAD-X
    Strategy(slicing=Teapot(2), element_type=xt.Bend),
    Strategy(slicing=Teapot(n_slice_arc_quad), element_type=xt.Quadrupole),
    Strategy(slicing=Teapot(1), element_type=xt.Sextupole),
    Strategy(slicing=Teapot(1), element_type=xt.Octupole),
    # Quad with betas above 5000 m
    Strategy(slicing=Teapot(200), name='qc1l2.*'),
    Strategy(slicing=Teapot(200), name='qc1r3.*'),
    Strategy(slicing=Teapot(200), name='qc1r2.*'),
    Strategy(slicing=Teapot(200), name='qc1l1.*'),
    Strategy(slicing=Teapot(200), name='qc1l3.*'),
    Strategy(slicing=Teapot(200), name='qc5l.*'),
    Strategy(slicing=Teapot(200), name='qc0.*'),
    Strategy(slicing=Teapot(200), name='qc2r1.*'),
    Strategy(slicing=Teapot(200), name='qc3.*'),
    Strategy(slicing=Teapot(200), name='qc1r1.*'),
    Strategy(slicing=Teapot(200), name='qc4.*'),
    Strategy(slicing=Teapot(200), name='qa1.*'),
    Strategy(slicing=Teapot(200), name='qc2l1.*'),
    Strategy(slicing=Teapot(200), name='qc7l.*'),
    Strategy(slicing=Teapot(200), name='qc7.*'),
    Strategy(slicing=Teapot(200), name='qb1.*'),
    Strategy(slicing=Teapot(200), name='qc2r2.*'),
    Strategy(slicing=Teapot(200), name='qc2l2.*'),
    Strategy(slicing=Teapot(200), name='qc3l.*'),
    # Quads with betas above 2000 m
    Strategy(slicing=Teapot(100), name='qc0l.2'),
    Strategy(slicing=Teapot(100), name='qc4l.2'),
    Strategy(slicing=Teapot(100), name='qb5.2'),
    Strategy(slicing=Teapot(100), name='qa3.2'),
    Strategy(slicing=Teapot(100), name='qc6l.2'),
    Strategy(slicing=Teapot(100), name='qb6.2'),
    Strategy(slicing=Teapot(100), name='qb3.2'),
    Strategy(slicing=Teapot(100), name='qb4.2'),
    Strategy(slicing=Teapot(100), name='qi2.2'),
    Strategy(slicing=Teapot(100), name='qa2.2'),
    Strategy(slicing=Teapot(100), name='qb2.2'),
]

line.slice_thick_elements(slicing_strategies=slicing_strategies)

tw = line.twiss4d(strengths=True)

print(f'Qx thick: {tw_thick.qx}')
print(f'Qx thin:  {tw.qx}, error: {tw.qx - tw_thick.qx:.2e}')
print(f'Qy thick: {tw_thick.qy}')
print(f'Qy thin:  {tw.qy}, error: {tw.qy - tw_thick.qy:.2e}')

env['fccee_p_ring_thin'] = line

env.to_json(f'fccee_{lattice_config}_thick_thin.json.gz')

# Copy lattice and strengths to the main directory
import shutil
shutil.copy(f'fccee_{lattice_config}_thick_thin.json.gz', '..')
