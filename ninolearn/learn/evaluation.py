import numpy as np

from sklearn.metrics import mean_squared_error

from ninolearn.utils import scale
from scipy.stats import pearsonr


def explained_variance(y, pred, time):
    """
    Returns the explained variance (r^2) for each month in a time series
    """
    r = np.zeros(12)
    rsq = np.zeros(12)

    for i in range(12):
        month = (time.month == i+1)
        y_sel = scale(y[month])
        pred_sel = scale(pred[month])
        r[i] = np.corrcoef(y_sel, pred_sel)[0, 1]
        rsq[i] = round(r[i]**2, 3)
    return rsq

def seasonal_nll(y, pred_mean, pred_std, time, evaluate):
    score = np.zeros(12)
    for i in range(12):
        month = (time.month == i+1)
        y_sel = y[month]
        pred_mean_sel = pred_mean[month]
        pred_std_sel = pred_std[month]
        score[i] = evaluate(y_sel, pred_mean_sel, pred_std_sel)
    return score


def correlation(y, pred, time):
    """
    Returns the correlation (r) for each month in a time series
    """
    r = np.zeros(12)
    p = np.zeros(12)
    for i in range(12):
        month = (time.month == i+1)
        y_sel = scale(y[month])
        pred_sel = scale(pred[month])
        r[i], p[i] = pearsonr(y_sel, pred_sel)
    return r, p

def rmse_mon(y, pred, time):
    """
    Returns the RMSE for each month in a time series
    """
    RMSE = np.zeros(12)

    for i in range(12):
        month = (time.month == i+1)
        y_sel = y[month]
        pred_sel = pred[month]
        RMSE[i] = np.sqrt(mean_squared_error(y_sel, pred_sel))/np.std(y_sel)
    return RMSE


def rmse_monmean(y, predict, time):
    """
    Computes the root mean square error (RMSE)

    :param y: the base line data
    :param predict: the predicted data
    :return: the RMSE
    """
    seasonal_RMSE = rmse_mon(y, predict, time)
    return np.mean(seasonal_RMSE)

def rmse(y, predict):
    """
    Computes the root mean square error (RMSE)

    :param y: the base line data
    :param predict: the predicted data
    :return: the RMSE
    """
    return np.sqrt(mean_squared_error(y, predict))

def nrmse(y, predict):
        """
        Computes the nromalized root mean square error (NRMSE)

        :param y: the base line data
        :param predict: the predicted data
        :return: the NRMSE
        """
        return rmse(y, predict) / (np.max([y, predict])
                                         - np.min([y, predict]))


def inside_fraction(ytrue, ypred_mean, ypred_std, std_level=1):
    """
    Returns the fraction of how much of the true observation stayed in the
    confindence interval.

    :param ytrue: The true observation.
    :param ypred_mean: The mean of the prediction.
    :param ypred_std: The standard deviation of the prediction.
    :param std_level: The standard deviation of the confidence interval
    :return: The fraction  of the observation that is in the confidence
    interval
    """
    ypred_max = ypred_mean + ypred_std * std_level
    ypred_min = ypred_mean - ypred_std * std_level

    in_or_out = np.zeros((len(ypred_mean)))
    in_or_out[(ytrue>ypred_min) & (ytrue<ypred_max)] = 1
    in_frac = np.sum(in_or_out)/len(ytrue)

    return in_frac
