# Module to run tests on pyigm.utils

from __future__ import print_function, absolute_import, division, unicode_literals

# TEST_UNICODE_LITERALS

import pytest
import numpy as np

from astropy.cosmology import Planck15 as cosmo
from astropy.coordinates import SkyCoord
from astropy import units as u
import astropy

from pyigm.utils import calc_rho
from pyigm.utils import calc_Galactic_rho


def test_calcrho():
    # Single
    coord1 = SkyCoord(ra=100., dec=50., unit='deg')
    z2=0.2
    coord2 = SkyCoord(ra=100., dec=50.001, unit='deg')
    # Calc
    rho, angle = calc_rho(coord1, coord2, z2, cosmo)
    # Test
    assert np.isclose(rho.value, 12.2587523534)
    assert rho.unit == astropy.units.kpc
    assert isinstance(angle, astropy.coordinates.Angle)
    # Comoving
    rho, angle = calc_rho(coord1, coord2, z2, cosmo, comoving=True)
    assert np.isclose(rho.value, 14.71050271)

    # One and many
    coords2 = SkyCoord(ra=[100., 100.], dec=[50.001,49.998], unit='deg')
    z2 = np.array([0.2,0.2])
    rhos, angles = calc_rho(coord1, coords2, z2, cosmo)
    assert rhos.size == 2
    np.isclose(2 * rhos[0].value, rhos[1].value, rtol=1e-4)

    # Many and many
    coords1 = SkyCoord(ra=[100., 100.], dec=[50.00,49.999], unit='deg')
    z2 = np.array([0.2,0.3])
    rhos3, angles3 = calc_rho(coords1, coords2, z2, cosmo)
    assert np.isclose(angles3[0].value,angles3[1].value, rtol=1e-6)
    assert rhos3[1] > rhos3[0]


def test_calcrho_lowz():
    """ Also tickles velcorr_mould
    """
    # Single
    coord1 = SkyCoord(ra=100., dec=50., unit='deg')
    z2=0.02
    coord2 = SkyCoord(ra=100., dec=50.001, unit='deg')
    # Calc
    rho, angle = calc_rho(coord1, coord2, z2, cosmo)
    np.isclose(rho.value, 1.5391395565522688)


def test_calc_Galactic_rho():
    # Galactic
    coord = SkyCoord(l=0.*u.deg, b=0.*u.deg, frame='galactic')
    rho2, angle2 = calc_Galactic_rho(coord)
    assert np.isclose(rho2.value, 0.)
    assert np.isclose(angle2.value, 0.)
    coord = SkyCoord(l=45.*u.deg, b=45.*u.deg, frame='galactic')
    rho3, angle3 = calc_Galactic_rho(coord)
    assert np.isclose(rho3.value, 6.928203230275509)
# Module to run tests on initializing AbslineSystem

# TEST_UNICODE_LITERALS

import numpy as np
import copy
import pytest

import astropy.units as u
from astropy.cosmology import FlatLambdaCDM, LambdaCDM

from pyigm.utils import cosm_xz

'''
def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'files')
    return os.path.join(data_dir, filename)
'''

def test_dxdz():
    # Default cosmology (Vanilla)
    Xz = cosm_xz(3.)
    np.isclose(Xz, 7.68841320742732)
    dxdz = cosm_xz(3., flg_return=1)
    np.isclose(dxdz, 3.5847294011983)
    # Open
    copen = LambdaCDM(H0=70., Om0=0.3, Ode0=0.)
    dxdz = cosm_xz(3., cosmo=copen, flg_return=1)
    np.isclose(dxdz, 2.90092902756)

