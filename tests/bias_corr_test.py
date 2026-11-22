from tank_core.bias_correction import gqm
from pathlib import Path
import numpy as np
import pandas as pd


def bern_gamma_sample(rng, n, dry_frac, a, b):
    #: dry days = 0, wet days ~ gamma(a, b)
    data = rng.gamma(a, b, n)
    data[rng.random(n) < dry_frac] = 0
    return data


def test_gqm():
    sample_data_path = Path(__file__).absolute().parent

    data = pd.read_csv(sample_data_path / 'test_data' / 'biascorr_dat.csv')

    _gqm = gqm()

    _gqm.fit(data['obs'].values,data['sim'].values)

    corr = _gqm.correct(data['sim'])

    assert np.all(np.isfinite(corr))
    assert np.all(corr >= 0)
    assert np.isclose(corr.mean(), data['obs'].mean(), rtol=0.05)


def test_gqm_synthetic():
    #: model with drizzle (fewer dry days) and wrong intensity
    rng = np.random.default_rng(42)
    obs = bern_gamma_sample(rng, 20000, dry_frac=0.4, a=0.8, b=8.0)
    sim = bern_gamma_sample(rng, 20000, dry_frac=0.1, a=1.5, b=3.0)

    _gqm = gqm().fit(obs, sim)
    corr = _gqm.correct(sim)

    assert np.all(np.isfinite(corr))

    #: dry day fraction, mean and wet quantiles match observed
    assert np.isclose((corr <= 0.01).mean(), (obs <= 0.01).mean(), atol=0.02)
    assert np.isclose(corr.mean(), obs.mean(), rtol=0.05)
    for q in [50, 90, 99]:
        assert np.isclose(np.percentile(corr, q), np.percentile(obs, q), rtol=0.1)


def test_gqm_sim_dry_stays_dry():
    #: model with more dry days than observed
    rng = np.random.default_rng(0)
    obs = bern_gamma_sample(rng, 5000, dry_frac=0.2, a=0.8, b=8.0)
    sim = bern_gamma_sample(rng, 5000, dry_frac=0.6, a=0.8, b=8.0)

    corr = gqm().fit(obs, sim).correct(sim)

    assert np.all(corr[sim <= 0.01] == 0)


def test_gqm_extremes_finite_and_monotonic():
    data = pd.read_csv(Path(__file__).absolute().parent / 'test_data' / 'biascorr_dat.csv')
    _gqm = gqm().fit(data['obs'].values, data['sim'].values)

    #: up to ~70x of max simulated value (gamma.sf underflows at ~700x sim scale)
    x = np.linspace(0, 500, 2001)
    corr = _gqm.correct(x)

    assert np.all(np.isfinite(corr))
    assert np.all(np.diff(corr) >= 0)


def test_gqm_identity():
    #: same distribution for obs and sim -> no correction
    rng = np.random.default_rng(1)
    data = bern_gamma_sample(rng, 5000, dry_frac=0.3, a=0.8, b=8.0)

    _gqm = gqm().fit(data, data)
    x = np.array([0.5, 1, 5, 20, 100])

    assert np.allclose(_gqm.correct(x), x)


def test_gqm_set_params_and_scalar():
    data = pd.read_csv(Path(__file__).absolute().parent / 'test_data' / 'biascorr_dat.csv')
    fitted = gqm().fit(data['obs'].values, data['sim'].values)
    loaded = gqm().set_params(np.array(fitted.obs_param), np.array(fitted.sim_param))

    x = data['sim'].values
    assert np.allclose(loaded.correct(x), fitted.correct(x))
    assert np.isclose(fitted.correct(5.0), fitted.correct(np.array([5.0]))[0])
