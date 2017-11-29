# Module to run tests on initializing AbslineSystem

# TEST_UNICODE_LITERALS

import numpy as np
import copy
import pytest

import astropy.units as u
from astropy.cosmology import FlatLambdaCDM

from pyigm.fN.fnmodel import FNModel
from pyigm.fN import tau_eff as pyteff

'''
def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'files')
    return os.path.join(data_dir, filename)
'''

def test_lya_obs():
    # Float
    teff = pyteff.lyman_alpha_obs(1.)
    assert isinstance(teff, float)
    np.testing.assert_allclose(teff,0.0327531536838541)
    # Array
    teff = pyteff.lyman_alpha_obs(np.linspace(0., 4.5, 100))
    assert len(teff) == 100
    np.testing.assert_allclose(teff[-1], 1.21192628)
    # Extrap fail
    with pytest.raises(ValueError):
        teff = pyteff.lyman_alpha_obs(np.linspace(0., 5., 100))
    # Extrap ok
    teff = pyteff.lyman_alpha_obs(np.linspace(0., 5., 100), zmax=9.)

def test_teff():
    fN_default = FNModel.default_model()
    zval,teff_LL = pyteff.lyman_limit(fN_default, 0.5, 2.45)
    #
    np.testing.assert_allclose(zval[0], 0.5)
    np.testing.assert_allclose(teff_LL[0], 1.8197, rtol=1e-4) # scipy 0.19

def test_lya():
    # f(N)
    fN_model = FNModel.default_model()

    # tau_eff
    lamb = 1215.6701*(1+2.4)
    teff = pyteff.lyman_ew(lamb, 2.5, fN_model, NHI_MIN=12., NHI_MAX=17.)
    # Test
    #np.testing.assert_allclose(teff, 0.19821452949713764)
    np.testing.assert_allclose(teff, 0.19827, atol=1e-3)  # scipy 0.19
    # Change cosmology
    cosmo = FlatLambdaCDM(H0=60, Om0=0.2)
    fN_model2 = FNModel.default_model(cosmo=cosmo)
    teff2 = pyteff.lyman_ew(lamb, 2.5, fN_model2, NHI_MIN=12., NHI_MAX=17.)
    np.testing.assert_allclose(teff2, 0.2381, atol=3e-4)


def test_lyx():
    # f(N)
    fN_model = FNModel.default_model()

    # tau_eff
    lamb = 917.*(1+2.4)
    teff = pyteff.lyman_ew(lamb, 2.5, fN_model, NHI_MIN=12., NHI_MAX=17.)
    # Test
    np.testing.assert_allclose(teff, 0.234765, rtol=2e-4)  # scipy 0.19


def test_parallel():
    import multiprocessing
    from linetools.lists.linelist import LineList
    # f(N)
    fN_model = FNModel.default_model()
    # Lines
    HI = LineList('HI')
    tst_wv = u.Quantity(HI._data['wrest'])
    #
    adict = []
    for wrest in tst_wv:
        tdict = dict(ilambda=wrest.value*(1+2.4), zem=2.5, fN_model=fN_model, wrest=copy.deepcopy(tst_wv))
        adict.append(tdict)

    pool = multiprocessing.Pool(2) # initialize thread pool N threads
    ateff = pool.map(pyteff.map_lymanew, adict)
    # Test
    np.testing.assert_allclose(ateff[-3:],
                               np.array([0.238569, 0.206972,  0.225049]),
                               atol=3e-4)

def test_DM():
    DM = pyteff.DM(1.)
    assert DM.unit == u.pc/u.cm**3
    np.testing.assert_allclose(DM.value, 1235.83, rtol=2e-5)



