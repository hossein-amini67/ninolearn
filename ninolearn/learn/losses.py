import keras.backend as K

def nll_gaussian(y_true, y_pred):
    """
    Negative - log -likelihood for the prediction of a gaussian probability
    """
    mean = y_pred[:,0]
    sigma = y_pred[:,1] + 1e-6 # adding 1-e6 for numerical stability reasons

    first  =  0.5 * K.log(K.square(sigma))
    second =  K.square(y_true[:,0] - mean) / (2  * K.square(sigma))
    summed = first + second

    loss =  K.mean(summed, axis=-1)
    return loss


def nll_skewed_gaussian(y_true, y_pred):
    """
    Negative - log -likelihood for the prediction of a gaussian probability
    """
    mean = y_pred[:,0]
    sigma = y_pred[:,1] + 1e-6 # adding 1-e6 for numerical stability reasons
    alpha = y_pred[:,2]

    first  =  0.5 * K.log(K.square(sigma))

    second =  K.square(y_true[:,0] - mean) / (2  * K.square(sigma))

    x = (y_true[:,0] - mean) / sigma
    arg_erf = (1 +  K.tf.math.erf(alpha * 0.5**0.5  * x)) + 1e-8 # adding 1-e8 for numerical stability reasons
    third = -  K.log(arg_erf)

    summed = first + second + third

    loss =  K.mean(summed, axis=-1)

    return loss
