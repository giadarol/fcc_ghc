import xtrack as xt
import numpy as np

env = xt.Environment.from_json('../fccee_z_thick_thin.json.gz')

env['freq400_1'] = 400.7871323229729
env['lag400_1'] = 0.4
env['volt400_1'] = 13.2 * 6 / 14
env['on_rf400_1'] = 1.
env['l400_1'] = 11.24
env['ldrf'] = 0.5 # Need to extend with thick cavities

env.new('ac400_1', 'Cavity', frequency='freq400_1 * 1e6',
        lag='lag400_1 * 360.', voltage='volt400_1 * on_rf400_1 * 1e6')

line = env.fccee_p_ring

# Remove all presently installed cavities with name starting with ca1
line.discard_tracker()
tt = line.get_table()
tt_cav = tt.rows[tt.element_type == 'Cavity'].rows['ca1.*']
for nn in tt_cav.name:
    line.remove(nn)

# Install RF cryomodules modules at Z optics
# Note that the cavities should be installed on the right side of the Insertion (clockwise beam)
# so they are after the beam crossing and on the inside path already.
# This needs rematching the insertion for a more symmmetric optics

line.insert([
    env.new('s.rfins', 'Marker', at='lbwr/2.', from_='bwr.3'),
    env.new('e.rfins', 'Marker', at='-lbri1/2.', from_='bri1.3'),

    env.new('ac400_1.1', 'ac400_1', at='3.5 + 1*ldrf + 0.5*l400_1', from_='qrfr1.3'),
    env.new('ac400_1.2', 'ac400_1', at='3.5 + 2*ldrf + 1.5*l400_1', from_='qrfr1.3'),
    env.new('ac400_1.3', 'ac400_1', at='3.5 + 3*ldrf + 2.5*l400_1', from_='qrfr1.3'),
    env.new('ac400_1.4', 'ac400_1', at='3.5 + 4*ldrf + 3.5*l400_1', from_='qrfr1.3'),

    env.new('ac400_1.5', 'ac400_1', at='3.5 + 1*ldrf + 0.5*l400_1', from_='qrdr1.3'),
    env.new('ac400_1.6', 'ac400_1', at='3.5 + 2*ldrf + 1.5*l400_1', from_='qrdr1.3'),
    env.new('ac400_1.7', 'ac400_1', at='3.5 + 3*ldrf + 2.5*l400_1', from_='qrdr1.3'),
    env.new('ac400_1.8', 'ac400_1', at='3.5 + 4*ldrf + 3.5*l400_1', from_='qrdr1.3'),

    env.new('ac400_1.9',  'ac400_1', at='3.5 + 1*ldrf + 0.5*l400_1', from_='qrfr2.3'),
    env.new('ac400_1.10', 'ac400_1', at='3.5 + 2*ldrf + 1.5*l400_1', from_='qrfr2.3'),
    env.new('ac400_1.11', 'ac400_1', at='3.5 + 3*ldrf + 2.5*l400_1', from_='qrfr2.3'),
    env.new('ac400_1.12', 'ac400_1', at='3.5 + 4*ldrf + 3.5*l400_1', from_='qrfr2.3'),

    env.new('ac400_1.13', 'ac400_1', at='3.5 + 1*ldrf + 0.5*l400_1', from_='qrdr2.3'),
    env.new('ac400_1.14', 'ac400_1', at='3.5 + 2*ldrf + 1.5*l400_1', from_='qrdr2.3'),
], s_tol=1e-8)

# Install cavities also in the thin line, if present
if 'fccee_p_ring_thin' in env.lines:

    # remove all cavities from the thin line
    env.fccee_p_ring_thin.discard_tracker()
    tt = env.fccee_p_ring_thin.get_table()
    tt_cav = tt.rows[tt.element_type == 'Cavity']
    for nn in tt_cav.name:
        env.fccee_p_ring_thin.remove(nn)

    # Install all cavities in the thick line also in the thin line
    tt_thick = line.get_table()
    tt_cav_in_thick = tt_thick.rows[tt_thick.element_type == 'Cavity']
    insertions = []
    for nn in tt_cav_in_thick.name:
        insertions.append(env.place(nn, at=tt_thick['s', nn]))
    env.fccee_p_ring_thin.insert(insertions)
