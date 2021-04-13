import tensorflow as tf
import tensorflow.keras.backend as K


__author__ = ['Giuseppe Filitto']
__email__ = ['giuseppe.filitto@studio.unibo.it']


def dice_coef(y_true, y_pred, smooth=1):
    '''

    Dice coefficient, also know as Sørensen-Dice index, is used to gauge the similarity of two samples. Given 2 sets it is defined as  twice the number of elements common to both sets divided by the sum of the number of elements in each set.

    Parameters
    ----------
    y_true : Tensor
        input tensor with shape: [batch_size, height, width, channels].
    y_pred : Tensor
        predicted tensor with shape: [batch_size, height, width, channels].
    smooth : int, float, optional
        value that will be added to the numerator and denominator to avoid 0 division, by default 1.

    Returns
    -------
    dice: float
        dice coefficient. The index is a number between 0 and 1 , if 1 sets totally match.

    References
    -----------
    - Wiki https://en.wikipedia.org/wiki/Sørensen–Dice_coefficient


    '''

    intersection = K.sum(y_true * y_pred, axis=[1, 2, 3])
    total = K.sum(y_true, axis=[1, 2, 3]) + K.sum(y_pred, axis=[1, 2, 3])
    dice = K.mean((2. * intersection + smooth) / (total + smooth), axis=0)
    return dice


def iou(y_true, y_pred, smooth=1):
    '''

    Intersection over union (IoU) also know as Jaccard coefficient, measures similarity between finite sample sets. Defined as the size of the intersection divided by the size of the union of the sample sets.

    Parameters
    ----------
    y_true : Tensor
        input tensor with shape: [batch_size, height, width, channels].
    y_pred : Tensor
        predicted tensor with shape: [batch_size, height, width, channels].
    smooth : int, float, optional
        value that will be added to the numerator and denominator to avoid 0 division, by default 1.

    Returns
    -------
    iou: float
        Intersection over union. The index is a number between 0 and 1 , if 1 sets totally match.

    References
    -----------
    - Wiki https://en.wikipedia.org/wiki/Jaccard_index


    '''

    intersection = K.sum(y_true * y_pred, axis=[1, 2, 3])
    union = K.sum(y_true, axis=[1, 2, 3]) + \
        K.sum(y_pred, axis=[1, 2, 3]) - intersection
    iou = K.mean((intersection + smooth) / (union + smooth), axis=0)
    return iou


def iou_loss(y_true, y_pred):
    '''

    Also know as Jaccard distance, measures dissimilarity between sample sets, is complementary to the Jaccard coefficient and is obtained by subtracting the Jaccard coefficient from 1, or, equivalently, by dividing the difference of the sizes of the union and the intersection of two sets by the size of the union.

    Parameters
    ----------
    y_true : Tensor
        input tensor with shape: [batch_size, height, width, channels].
    y_pred : Tensor
        predicted tensor with shape: [batch_size, height, width, channels].

    References
    -----------
    - Wiki https://en.wikipedia.org/wiki/Jaccard_index


    '''

    iou = iou(y_true, y_pred)
    return 1 - iou


def tversky_index(y_true, y_pred, smooth=1, alpha=0.7):
    '''

     The Tversky index is an asymmetric similarity measure on sets that compares a variant to a prototype. The Tversky index can be seen as a generalization of the Sørensen–Dice coefficient and the Jaccard index. Setting alpha = beta = 1 produces the jaccard coefficient, setting alpha = beta = 0.5 produces the Sørensen–Dice coefficient


    Parameters
    ----------
    y_true : Tensor
        input tensor with shape: [batch_size, height, width, channels].
    y_pred : Tensor
        predicted tensor with shape: [batch_size, height, width, channels].
    smooth : int, float, optional
        value that will be added to the numerator and denominator to avoid 0 division, by default 1.
    alpha: float, optional
        parameter  of the Tversky index, by default 0.7.

    Returns
    -------
    tversky: float
        Tversky index. The index is a number between 0 and 1 , if 1 sets totally match.

    References
    -----------
    - Wiki https://en.wikipedia.org/wiki/Tversky_index


    '''

    beta = 1 - alpha  # since alpha + beta = 1 cases are of more interest

    true_pos = K.sum(y_true * y_pred, axis=[1, 2, 3])
    false_neg = K.sum(y_true * (1 - y_pred), axis=[1, 2, 3])
    false_pos = K.sum((1 - y_true) * y_pred, axis=[1, 2, 3])
    tversky = K.mean((true_pos + smooth)/(true_pos + alpha *
                                          false_neg + beta * false_pos + smooth), axis=0)

    return tversky


def tversky_loss(y_true, y_pred):
    '''

     Measure of dissimilarity between sample sets, is complementary to the Tversky index and is obtained by subtracting the Tversky index from 1.

    Parameters
    ----------
    y_true : Tensor
        input tensor with shape: [batch_size, height, width, channels].
    y_pred : Tensor
        predicted tensor with shape: [batch_size, height, width, channels].

    References
    -----------
    - https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8759329

    '''

    T = tversky_index(y_true, y_pred)

    return 1 - T


def focal_tversky_loss(y_true, y_pred, gamma=1.33):
    '''

   Generalized focal loss function based on the Tversky index to address the issue of data imbalance in medical image segmentation.

    Parameters
    ----------
    y_true : Tensor
        input tensor with shape: [batch_size, height, width, channels].
    y_pred : Tensor
        predicted tensor with shape: [batch_size, height, width, channels].
    gamma: float
        control parameter, by default 1.33. Proposed in range [1,3].

    References
    -----------
    - https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8759329

    '''

    T = tversky(y_true, y_pred)

    return K.pow((1-T), 1/gamma)
