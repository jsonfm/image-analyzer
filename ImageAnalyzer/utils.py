import cv2
import numpy as np
import pydicom
import time
import cython


# 1. Dibujar el ROI
# 2. Calcular el área
# 3. Calcular el Volumen
# 4. Recalcular el umbral

def roi_mask(img=None, contours=None):
    """It applies a mask to a ROI and returns pixels data inside that region
    :param img: image array
    :param contours: contours list/array
    :return roi: image array with only roi data
    """
    roi = None
    if isinstance(img, np.ndarray) and isinstance(contours, (list, np.ndarray)):          
        mask = np.zeros_like(img)
        roi = np.zeros_like(img)
        cv2.drawContours(mask, contours, -1, 255, -1)
        roi[mask == 255] = img[mask == 255]
    return roi


def linearConvert(img):
    """It applies a linear conversion to an image array
    :param img: image array
    :return new_img: image array scaled
    """
    factor = 255 / (np.max(img) - np.min(img))
    new_img = factor * img - (factor * np.min(img))
    return new_img


def threshold_roi(roi=None, threshold=100, mode="Higher"):
    """It filters an image array with a threshold
    :param roi: image array
    :param threshold: threshold value
    :param mode: thresholding mode
    """
    if (mode == "Higher") and (roi is not None):
        roi[roi <= threshold] = 0
    elif (mode == "Lower") and (roi is not None):
        roi[roi >= threshold] = 0
    else:
        raise Exception("Mode is not valid! Please give a valid mode: 'higher' or 'lower'")
    return roi


def color_roi(roi):
    """It colorize a roi region with a pixma"""
    roi = cv2.applyColorMap(roi, cv2.COLORMAP_INFERNO)
    roi[roi < 5] = 0
    return roi


def draw_roi(img=None, contours=None, threshold=100, mode="Higher"):
    """It draws a ROI on an image array
    :param img: image array
    :param contours: contours list/array
    :param threshold: a value to filter values inside the roi
    :param mode: it select which mode of thresholding
    """
    roi = roi_mask(img, contours)
    roi = threshold_roi(roi, threshold, mode)
    if (roi is not None) and (img is not None) and (contours is not None):
        if len(img.shape) < 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if len(roi.shape) < 3:
            roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
        roi = color_roi(roi)

        img[roi > 0] = roi[roi > 0]
        return img
    return None


# path = "/home/jason/Documentos/Python/TESIS/anonymize/Anonymized - 140/Encefalo + Col Cervical/eFLAIR_longTR - 602/IM-0200-0001-0001.dcm"
# contours = np.load("conturstest.npy")
# dcm = pydicom.dcmread(path)
# img = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept
# img = linearConvert(img).astype(np.uint8)
# cnts = np.load("conturstest.npy")
#
# t0 = time.time()
# new = draw_roi(img, cnts, threshold=0)
# t1 = time.time()
# print("Eleapsed: ", t1 - t0)
# new = cv2.resize(new, dsize=(500, 500))
#
# cv2.imshow("roi ", new)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
