
import pandas as pd
import os
import numpy as np
import SimpleITK as sitk
from skimage import metrics


def volumeContour(imgA):
    value = imgA.sum()
    return value

def dice_coef(imgA, imgB):
    if imgA.shape != imgB.shape:
        raise ValueError("Shape mismatch: img and img2 must have to be of the same shape.")
    else:
        intersection = np.logical_and(imgA, imgB)
        value = (2. * intersection.sum()) / (imgA.sum() + imgB.sum())
    return value

def PPV_coef(imgA, imgB):
    if imgA.shape != imgB.shape:
        raise ValueError("Shape mismatch: img and img2 must have to be of the same shape.")
    else:
        intersection = np.logical_and(imgA, imgB)
        value = intersection.sum() / imgB.sum()
    return value

def Sens_coef(imgA, imgB):
    if imgA.shape != imgB.shape:
        raise ValueError("Shape mismatch: img and img2 must have to be of the same shape.")
    else:
        intersection = np.logical_and(imgA, imgB)
        diferencia = np.logical_and(imgA, np.logical_not(imgB))
        value = intersection.sum() / (diferencia.sum() + intersection.sum())
    return value


def bool_map(image):
  bool_map = np.zeros(image.shape, dtype=np.bool_)
  for z in range(image.shape[0]):
    for row in range(image.shape[1]):
        for col in range(image.shape[2]):
            if image[z,row,col] > 0:
                bool_map[z,row,col] = True
  return bool_map
