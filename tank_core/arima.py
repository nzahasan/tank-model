# -*- coding: utf-8 -*-
'''
Time series error Correction Module for model
---------------------------------------------
ARIMA(p,d,q)
    p - auto-regressive part
    d - integrated part / differentiation part
    q - moving average part

Order selection:
    d   - smallest d where ADF rejects unit root and KPSS does not strongly reject stationarity
    p,q - lowest AIC with d fixed

'''
import pickle
import warnings
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, kpss


class autoARIMA:

    '''
    A wrapper of statsmodels ARIMA for easier model fitting and generating forecast.
    d is chosen with ADF + KPSS unit root tests, then (p,q) by grid search with lowest
    AIC (Akaike Information Criteria). AIC is only comparable for the same d, so d is fixed first.
    '''

    def __init__(self,help_text=True):
        self.help_text    = help_text
        self.best_model   = None


    def get_d(self, _endog, max_d, adf_alpha, kpss_alpha):

        # ADF H0: unit root, KPSS H0: stationary
        # stationary when ADF rejects unit root, unless KPSS strongly rejects stationarity
        # (KPSS at alpha alone falsely rejects too often and leads to over-differencing)
        x = _endog[~np.isnan(_endog)]

        for d in range(max_d+1):

            x_diff = np.diff(x, n=d)

            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                adf_p  = adfuller(x_diff,autolag='AIC')[1]
                kpss_p = kpss(x_diff,regression='c',nlags='auto')[1]

            if adf_p < adf_alpha and kpss_p > kpss_alpha:
                return d


        return max_d


    def fit_model(self, endog, max_p=3, max_d=2, max_q=3, adf_alpha=0.05, kpss_alpha=0.01, maxiter=1000):

        # statsmodels clips kpss p-value to [0.01, 0.1], alpha outside that breaks get_d
        if not 0.01 <= kpss_alpha < 0.1:
            raise ValueError('kpss_alpha must be within [0.01, 0.1)')

        _endog = np.asarray(endog,dtype=float)

        d = self.get_d(_endog, max_d, adf_alpha, kpss_alpha)

        # trend candidates for the selected d
        #   d == 0 : no trend or constant (mean)
        #   d == 1 : no trend or drift ('t' in levels = constant in differences)
        #   d >= 2 : no trend
        if d == 0:
            trends = ['n','c']
        elif d == 1:
            trends = ['n','t']
        else:
            trends = ['n']

        best    = None
        skipped = []

        # iterate through (trend,p,q) values with fixed d
        for trend in trends:
            for p in range(max_p+1):
                for q in range(max_q+1):
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore')
                            # default optimizer limit (50 iterations) is often too low for larger orders
                            res = ARIMA(_endog,order=(p,d,q),trend=trend).fit(method_kwargs={'maxiter':maxiter})
                    except (ValueError,np.linalg.LinAlgError):
                        # unable to fit - skip
                        skipped.append((p,d,q,trend))
                        continue

                    # non-converged fit (unreliable AIC) - skip
                    if not res.mle_retvals.get('converged',True) or not np.isfinite(res.aic):
                        skipped.append((p,d,q,trend))
                        continue

                    # roots on/near the unit circle (bogus low aic) - skip
                    if np.any(np.abs(res.arroots) <= 1.01) or np.any(np.abs(res.maroots) <= 1.01):
                        skipped.append((p,d,q,trend))
                        continue

                    if best is None or res.aic < best.aic:
                        best = res

        if best is None:
            raise RuntimeError(f'No ARIMA order converged with d={d}')

        self.best_model = best

        if self.help_text == True:
            print(f'Lowest AIC value {best.aic:.3f} with order {best.model.order}, trend {best.model.trend}')
            if skipped:
                print(f'Skipped orders (failed, not converged or unit root): {skipped}')

        return self


    def forecast(self,num_step,alpha=0.05):

        # returns forecasted values and confidence limit of the forecast

        if self.best_model is None:
            raise RuntimeError('Fit the model first')

        fc = self.best_model.get_forecast(steps=num_step)

        return (np.asarray(fc.predicted_mean),np.asarray(fc.conf_int(alpha=alpha)))

    def in_sample_plot(self):

        from statsmodels.graphics.tsaplots import plot_predict

        plot_predict(self.best_model)
        return self

    def save_model(self, fileName):
        with open(fileName,'wb') as outModelFile:
            pickle.dump(self,outModelFile,pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load_model(cls, fileName):
        # returns the loaded model, allows autoARIMA.load_model(f).forecast(n)
        with open(fileName,'rb') as inModelFile:
            loaded = pickle.load(inModelFile)

        if not isinstance(loaded,cls):
            raise TypeError(f'{fileName} does not contain an autoARIMA model')

        return loaded
