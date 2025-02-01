# 400 MHz cavities double cell for W, ZH and tt poles

# cryomodule length = 11.24 (bride � bride)
# intercryomodule distance = 0.5
# 4 cavities per cryomodule; 2 cells per cavity

# V. Parma counts
# 7 cryomodules between quadrupoles fills : 81.68 m;
# add a quadrupole of 3.1 m plus 0.5 m on either side, hence half cell length at 85.78 m
# But the Quadrupoles QRF are only 2m long

# 52m half cell length, -2m of quadrupole length fits only 4 cryomodules. hence not enough space!
#s 52m free space in GHC optics;

import xtrack as xt

env = xt.get_environment()

env['freq400_2'] = 400.786682146657
env['lag400_2']  = 0.4
env['volt400_2'] = 13.2 * 6 / 33
env['on_rf400_2'] = 1.
env['l400_2'] = 11.24
env['ldrf'] = 0.5

env.new('ac400_2', 'Cavity', frequency='freq400_2 * 1e6',
        lag='lag400_2 * 360.', voltage='volt400_2 * on_rf400_2 * 1e6')

# and install 33 ac400_2 per beam at z and w pole and 2 times 33 ac400_2 on
# common line at zh pole

line = env.fccee_p_ring

# Remove all presently installed cavities with name starting with ca1
tt = line.get_table()
tt_cav = tt.rows[tt.element_type == 'Cavity'].rows['ca1.*']
line.remove(tt_cav.name)

# install rf cryomodules modules at w optics
# note that the cavities should be installed on the right side of the insertion (clockwise beam)
# so they are after the beam crossing and on the inside path already.
# this needs rematching the insertion for a more symmmetric optics

line.insert([
    env.new('s.rfins', 'Marker', at='lbwr/2.', from_='bwr.3'),
    env.new('e.rfins', 'Marker', at='-lbri1/2.', from_='bri1.3'),

    env.new('ac400_2.1',  'ac400_2', at='3.5 + 1*ldrf + 0.5*l400_2', from_='qrfr1.3'),
    env.new('ac400_2.2',  'ac400_2', at='3.5 + 2*ldrf + 1.5*l400_2', from_='qrfr1.3'),
    env.new('ac400_2.3',  'ac400_2', at='3.5 + 3*ldrf + 2.5*l400_2', from_='qrfr1.3'),
    env.new('ac400_2.4',  'ac400_2', at='3.5 + 4*ldrf + 3.5*l400_2', from_='qrfr1.3'),

    env.new('ac400_2.5',  'ac400_2', at='3.5 + 1*ldrf + 0.5*l400_2', from_='qrdr1.3'),
    env.new('ac400_2.6',  'ac400_2', at='3.5 + 2*ldrf + 1.5*l400_2', from_='qrdr1.3'),
    env.new('ac400_2.7',  'ac400_2', at='3.5 + 3*ldrf + 2.5*l400_2', from_='qrdr1.3'),
    env.new('ac400_2.8',  'ac400_2', at='3.5 + 4*ldrf + 3.5*l400_2', from_='qrdr1.3'),

    env.new('ac400_2.9',  'ac400_2', at='3.5 + 1*ldrf + 0.5*l400_2', from_='qrfr2.3'),
    env.new('ac400_2.10', 'ac400_2', at='3.5 + 2*ldrf + 1.5*l400_2', from_='qrfr2.3'),
    env.new('ac400_2.11', 'ac400_2', at='3.5 + 3*ldrf + 2.5*l400_2', from_='qrfr2.3'),
    env.new('ac400_2.12', 'ac400_2', at='3.5 + 4*ldrf + 3.5*l400_2', from_='qrfr2.3'),

    env.new('ac400_2.13', 'ac400_2', at='3.5 + 1*ldrf + 0.5*l400_2', from_='qrdr2.3'),
    env.new('ac400_2.14', 'ac400_2', at='3.5 + 2*ldrf + 1.5*l400_2', from_='qrdr2.3'),
    env.new('ac400_2.15', 'ac400_2', at='3.5 + 3*ldrf + 2.5*l400_2', from_='qrdr2.3'),
    env.new('ac400_2.16', 'ac400_2', at='3.5 + 4*ldrf + 3.5*l400_2', from_='qrdr2.3'),

    env.new('ac400_2.17', 'ac400_2', at='3.5 + 1*ldrf + 0.5*l400_2', from_='qrfr3.3'),
    env.new('ac400_2.18', 'ac400_2', at='3.5 + 2*ldrf + 1.5*l400_2', from_='qrfr3.3'),
    env.new('ac400_2.19', 'ac400_2', at='3.5 + 3*ldrf + 2.5*l400_2', from_='qrfr3.3'),
    env.new('ac400_2.20', 'ac400_2', at='3.5 + 4*ldrf + 3.5*l400_2', from_='qrfr3.3'),

    env.new('ac400_2.21', 'ac400_2', at='3.5 + 1*ldrf + 0.5*l400_2', from_='qrdr3.3'),
    env.new('ac400_2.22', 'ac400_2', at='3.5 + 2*ldrf + 1.5*l400_2', from_='qrdr3.3'),
    env.new('ac400_2.23', 'ac400_2', at='3.5 + 3*ldrf + 2.5*l400_2', from_='qrdr3.3'),
    env.new('ac400_2.24', 'ac400_2', at='3.5 + 4*ldrf + 3.5*l400_2', from_='qrdr3.3'),

    env.new('ac400_2.25', 'ac400_2', at='3.5 + 1*ldrf + 0.5*l400_2', from_='qrfr4.3'),
    env.new('ac400_2.26', 'ac400_2', at='3.5 + 2*ldrf + 1.5*l400_2', from_='qrfr4.3'),
    env.new('ac400_2.27', 'ac400_2', at='3.5 + 3*ldrf + 2.5*l400_2', from_='qrfr4.3'),
    env.new('ac400_2.28', 'ac400_2', at='3.5 + 4*ldrf + 3.5*l400_2', from_='qrfr4.3'),

    env.new('ac400_2.29', 'ac400_2', at='3.5 + 1*ldrf + 0.5*l400_2', from_='qrdr4.3'),
    env.new('ac400_2.30', 'ac400_2', at='3.5 + 2*ldrf + 1.5*l400_2', from_='qrdr4.3'),
    env.new('ac400_2.31', 'ac400_2', at='3.5 + 3*ldrf + 2.5*l400_2', from_='qrdr4.3'),
    env.new('ac400_2.32', 'ac400_2', at='3.5 + 4*ldrf + 3.5*l400_2', from_='qrdr4.3'),

    env.new('ac400_2.33', 'ac400_2', at='3.5 + 1*ldrf + 0.5*l400_2', from_='qrfr5.3'),
], s_tol=1e-8)


# Install cavities also in the thin line, if present
if 'fccee_p_ring_thin' in env.lines:

    # remove all cavities from the thin line
    tt = env.fccee_p_ring_thin.get_table()
    tt_cav = tt.rows[tt.element_type == 'Cavity']
    env.fccee_p_ring_thin.remove(tt_cav.name)

    # Install all cavities in the thick line also in the thin line
    tt_thick = line.get_table()
    tt_cav_in_thick = tt_thick.rows[tt_thick.element_type == 'Cavity']
    env.fccee_p_ring_thin.insert(
        [env.place(nn, at=tt_thick['s', nn]) for nn in tt_cav_in_thick.name])
