# Utility

import numpy as np

from os import listdir, mkdir, sep
from os.path import join, exists, splitext
# from scipy.misc import imread, imsave, imresize
# ImportError: cannot import name 'imread' from 'scipy.misc'
# https://github.com/titu1994/Neural-Style-Transfer/issues/59#issuecomment-515782686
import skimage
import skimage.io
import skimage.transform
import tensorflow as tf
from PIL import Image
from functools import reduce

import numpy as np
import imageio
from PIL import Image
from skimage import color


def imread(path, mode="RGB"):
    # Loads data in HxW format, then transposes to correct format
    img = np.array(imageio.imread(path, pilmode=mode))
    return img


def imresize(img, size, interp='bilinear'):
    """
    Resizes an image
    :param img:
    :param size: (Must be H, W format !)
    :param interp:
    :return:
    """
    if interp == 'bilinear':
        interpolation = Image.BILINEAR
    elif interp == 'bicubic':
        interpolation = Image.BICUBIC
    else:
        interpolation = Image.NEAREST

    # Requires size to be HxW
    size = (size[1], size[0])

    if type(img) != Image:
        img = Image.fromarray(img, mode='RGB')

    img = np.array(img.resize(size, interpolation))
    return img


def imsave(path, img):
    imageio.imwrite(path, img)
    return


def list_images(directory):
    images = []
    for file in listdir(directory):
        name = file.lower()
        if name.endswith('.png'):
            images.append(join(directory, file))
        elif name.endswith('.jpg'):
            images.append(join(directory, file))
        elif name.endswith('.jpeg'):
            images.append(join(directory, file))
    return images


def get_train_images(paths, resize_len=512, crop_height=256, crop_width=256, flag=True):
    if isinstance(paths, str):
        paths = [paths]

    images = []
    ny = 0
    nx = 0
    for path in paths:
        image = imread(path, mode='L')

        if flag:
            image = np.stack(image, axis=0)
            image = np.stack((image, image, image), axis=-1)
        else:
            image = np.stack(image, axis=0)
            image = np.stack(image, axis=-1)

        images.append(image)
    images = np.stack(images, axis=-1)

    return images


def get_images(paths, height=None, width=None):
    if isinstance(paths, str):
        paths = [paths]

    images = []
    for path in paths:
        image = imread(path, mode='RGB')

        if height is not None and width is not None:
            image = imresize(image, [height, width], interp='nearest')

        images.append(image)

    images = np.stack(images, axis=0)
    print('images shape gen:', images.shape)
    return images


def save_images(paths, datas, save_path, prefix=None, suffix=None):
    if isinstance(paths, str):
        paths = [paths]

    assert (len(paths) == len(datas))

    if not exists(save_path):
        mkdir(save_path)

    if prefix is None:
        prefix = ''
    if suffix is None:
        suffix = ''

    for i, path in enumerate(paths):
        data = datas[i]
        # print('data ==>>\n', data)
        data = data.reshape([data.shape[0], data.shape[1]])
        # print('data reshape==>>\n', data)

        name, ext = splitext(path)
        name = name.split(sep)[-1]

        path = join(save_path, prefix + suffix + ext)
        print('data path==>>', path)

        # new_im = Image.fromarray(data)
        # new_im.show()

        imsave(path, data)


def get_l2_norm_loss(diffs):
    shape = diffs.get_shape().as_list()
    size = reduce(lambda x, y: x * y, shape) ** 2
    sum_of_squared_diffs = tf.reduce_sum(tf.square(diffs))
    return sum_of_squared_diffs / size
