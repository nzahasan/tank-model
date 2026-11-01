import numpy as np
from statsmodels.tsa.arima_process import arma_generate_sample
from tank_core.arima import autoARIMA


def _integrated_ar1(n=400, seed=0):
    np.random.seed(seed)
    return np.cumsum(arma_generate_sample(ar=[1, -0.6], ma=[1], nsample=n))


def test_select_d():
    for seed in range(5):
        rng = np.random.default_rng(seed)
        assert autoARIMA(rng.standard_normal(400), helpText=False).getD() == 0
        assert autoARIMA(_integrated_ar1(seed=seed), helpText=False).getD() == 1


def test_fit_forecast():
    model = autoARIMA(_integrated_ar1(), helpText=False).fit()
    p, d, q = model.fitted_model.model.order

    assert d == 1
    assert p >= 1

    mean, conf = model.forecast(10)

    assert mean.shape == (10,)
    assert conf.shape == (10, 2)
    assert np.all(conf[:, 0] < mean) and np.all(mean < conf[:, 1])


def test_save_load(tmp_path):
    model = autoARIMA(_integrated_ar1(), helpText=False).fit()
    path = tmp_path / 'arima.pkl'

    model.saveModel(path)
    loaded = autoARIMA.loadModel(path)

    np.testing.assert_allclose(loaded.forecast(5)[0], model.forecast(5)[0])
