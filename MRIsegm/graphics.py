import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

__author__ = ['Giuseppe Filitto']
__email__ = ['giuseppe.filitto@studio.unibo.it']


def display(display_list, colormap=False, cmap='gist_heat', norm=True):
    '''

    Display a list of images: 'Input image', 'True Mask', 'Predicted mask'. It is possibile to show the predicted mask using matplotlib cmap setting colormap as True and if norm is set as True the image is normalized from 0. to 1.

    Parameters
    ----------
    display_list : list
        list of input image, true mask and predicted mask.
    colormap : bool, optional
        if True show the predicted mask using a seqeuntial colormap (i.e. matplotlib 'gist_heat'), by default False.
    cmap: str
        matplotlib cmap, by default 'gist_heat'.
    norm: bool, optional
        if normalized the predicted mask from 0. to 1., by deafult True.

    '''
    plt.style.use('default')
    plt.figure(figsize=(12, 8))
    title = ['Input image', 'True Mask', 'Predicted mask']
    for i in range(len(display_list)):
        plt.subplot(1, len(display_list), i + 1)
        plt.title(title[i])
        if i == 2 and colormap:
            ax = plt.gca()

            if norm:
                im = ax.imshow((display_list[i]),
                               cmap=cmap, vmin=0.0, vmax=1.0)
            else:
                im = ax.imshow((display_list[i]),
                               cmap=cmap)

            axins = inset_axes(ax, width="5%", height="100%", loc='lower left',
                               bbox_to_anchor=(1.02, 0., 1, 1), bbox_transform=ax.transAxes,
                               borderpad=0)

            plt.colorbar(im, cax=axins)

        else:
            # optional: tf.keras.preprocessing.image.array_to_img, just to rescale from 0.-1. to 0-255
            plt.imshow(tf.keras.preprocessing.image.array_to_img(
                display_list[i]), cmap='gray')
    plt.show()


def show_dataset(datagen, num=1):
    '''

    Show a given number of the first of a batch of data created using datagenerator (i.e. create_segmentation_generator_*).

    Parameters
    ----------
    datagen : iterator
         DirectoryIterator yielding tuples of (x, y) with shape (batch_size, height, width, channels) where x is the input image and y is the true mask.
    num : int, optional
        number of (x, y) tuples to be shown, by default 1.

    '''
    plt.style.use('default')
    for i in range(0, num):
        image, mask = next(datagen)
        display([image[0], mask[0]])


def plot_history(model_name, history, metrics, loss, save=True, custom_metrics=True, custom_loss=False, **kwargs):
    '''

    Show the model history such as metrics and loss for both training and validation using 'seaborn' style from matplotlib.

    Parameters
    ----------
    model_name : str
        name of the model. It is the suptitle of the plot.
    history : tf.keras History object
        result of model.fit(). it is a record of training loss values and metrics values at successive epochs, as well as validation loss values and validation metrics values (if applicable).
    metrics : list
        List of metrics to be evaluated by the model during training and testing. Each of this must be a string (name of a built-in function) or custom function (see MRIsegm.metrics).
    loss : string or a function
        string of name of a built-in function (i.e. 'binary_crossentropy' from tf.keras.metrics) or a custom function (see MRIsegm.losses).
    save : bool, optional
        if saving the plot to the given path which must be given as path='path/to/plot', by default True.
    custom_metrics : bool, optional
        if metrics are all custom function (see MRIsegm.metrics) or not (i.e. 'accuracy' from tf.keras.metrics), by default True.
    custom_loss : bool, optional
        if loss is a custom function (see MRIsegm.losses) or not (i.e. 'binary_crossentropy' from tf.keras.metrics), by default False.

    '''

    plt.style.use('seaborn')

    if kwargs.get('figsize'):
        figsize = kwargs.get('figsize')
    else:
        figsize = (18, 7)

    plt.figure(figsize=figsize)
    plt.suptitle('Model: ' + model_name, fontsize=15)

    if kwargs.get('labelsize'):
        labelsize = kwargs.get('labelsize')
        plt.rc('xtick', labelsize=labelsize)
        plt.rc('ytick', labelsize=labelsize)

    for i in range(len(metrics)):
        plt.subplot(1, len(metrics) + 1, i + 1)
        if custom_metrics:
            plt.plot(history.history['{}'.format(metrics[i].__name__)])
            plt.plot(history.history['val_' + '{}'.format(metrics[i].__name__)])
            plt.title('model  {}'.format(metrics[i].__name__), fontsize=15)
            plt.xlabel('epoch', fontsize=15)
            plt.ylabel('{}'.format(metrics[i].__name__), fontsize=15)
            plt.legend(['train', 'validation'], loc='best')

        else:
            plt.plot(history.history[metrics[i]])
            plt.plot(history.history['val_' + metrics[i]])
            plt.title('model ' + metrics[i], fontsize=15)
            plt.xlabel('epoch', fontsize=15)
            plt.ylabel(metrics[i], fontsize=15)
            plt.legend(['train', 'validation'], loc='best')

    if custom_loss:
        plt.subplot(1, len(metrics) + 1, len(metrics) + 1)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model {}'.format(loss.__name__), fontsize=15)
        plt.xlabel('epoch', fontsize=15)
        plt.ylabel('{}'.format(loss.__name__), fontsize=15)
        plt.legend(['train', 'validation'], loc='best')

    else:
        plt.subplot(1, len(metrics) + 1, len(metrics) + 1)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss', fontsize=15)
        plt.xlabel('epoch', fontsize=15)
        plt.ylabel(loss, fontsize=15)
        plt.legend(['train', 'validation'], loc='best')

    if save:
        path = kwargs.get('path')
        plt.savefig(path)
    plt.show()


def show_prediction(datagen, model, num=1, colormap=True, cmap='gist_heat', norm=True):
    '''

    Show a given number of [x, y, z] where x is the first input image, y the first true mask created using datagenerator (i.e create_segmentation_generator) and z is the predicted mask from x by the given model. The predicted mask is shown using a sequential colormap.

    Parameters
    ----------
    datagen : iterator
         DirectoryIterator yielding tuples of (x, y) with shape (batch_size, height, width, channels) where x is the input image and y is the true mask.
    model : Keras Model class
        model used to predict the mask.
    num : int, optional
        number of rows of images to be shown, by default 1.
    colormap : bool, optional
        if True the predicted mask is shown using a sequential colormap (i.e. matplotlib 'gist_heat'), by default True.
    cmap: str
        matplotlib cmap, by default 'gist_heat'.
    norm: bool, optional
        if normalized the predicted mask from 0. to 1., by deafult True.

    '''
    plt.style.use('default')
    for i in range(0, num):
        image, mask = next(datagen)
        pred_mask = model.predict(image)
        display([image[0], mask[0], pred_mask[0]], colormap, cmap, norm)


def display_predictions(display_list, keys, colormap=True, cmap='gist_heat', figsize=(25, 15)):
    plt.figure(figsize=figsize, constrained_layout=True)
    title = ['True Mask'] + keys
    for i in range(len(display_list)):
        plt.subplot(1, len(display_list), i + 1)
        plt.title(title[i])
        if i >= 1 and colormap:
            ax = plt.gca()
            im = ax.imshow((display_list[i]), cmap=cmap, vmin=0.0, vmax=1.0)
            if i == len(display_list) - 1:
                axins = inset_axes(ax, width="5%", height="100%", loc='lower left', bbox_to_anchor=(1.02, 0., 1, 1), bbox_transform=ax.transAxes, borderpad=0)
                plt.colorbar(im, cax=axins)
        else:
            plt.imshow(tf.keras.preprocessing.image.array_to_img(display_list[i]), cmap='gray')
            # optional: tf.keras.preprocessing.image.array_to_img, just to rescale from 0.-1. to 0-255

    plt.show()


def show_multiple_predictions(datagen, keys, values, num=1, colormap=True, cmap='gist_heat', figsize=(25, 15)):
    for i in range(0, num):
        image, mask = next(datagen)
        pred_masks = [model.predict(image) for model in values]
        disp_list = [mask[0]] + [pred_masks[j][0] for j in range(len(pred_masks))]
        display_predictions(disp_list, keys, colormap, cmap, figsize)
        plt.show()


def display_overlap(display_list, keys, colormap=True, cmap='gist_heat', figsize=(25, 15)):
    plt.figure(figsize=figsize, constrained_layout=True)
    title = ['True Mask'] + keys
    for i in range(1, len(display_list)):
        plt.subplot(1, len(display_list), i + 1)
        plt.title(title[i - 1])
        if i >= 2 and colormap:
            ax = plt.gca()
            im_0 = ax.imshow(display_list[0], cmap='gray', vmin=0.0, vmax=1.0)
            display_list[i][display_list[i] <= 0.05] = np.nan
            im = ax.imshow(display_list[i], cmap=cmap, vmin=0.0, vmax=1.0, alpha=0.75)
            if i == len(display_list) - 1:

                axins = inset_axes(ax, width="5%", height="100%", loc='lower left', bbox_to_anchor=(1.02, 0., 1, 1), bbox_transform=ax.transAxes, borderpad=0)
                plt.colorbar(im, cax=axins)
        else:
            plt.imshow(tf.keras.preprocessing.image.array_to_img(display_list[i] + display_list[0]), cmap='gray')
            # optional: tf.keras.preprocessing.image.array_to_img, just to rescale from 0.-1. to 0-255
    plt.show()


def show_multiple_overlap(datagen, keys, values, num=1, colormap=True, cmap='gray', figsize=(25, 15)):
    for i in range(0, num):
        image, mask = next(datagen)
        pred_masks = [model.predict(image) for model in values]
        disp_list = [image[0]] + [mask[0]] + [pred_masks[j][0] for j in range(len(pred_masks))]
        display_overlap(disp_list, keys, colormap, cmap, figsize)
        plt.show()
