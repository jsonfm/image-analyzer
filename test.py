import sys
from gui.components.viewer import Viewer
from gui.components.multipleROI import MultipleROI
from dataloaders.images import ImageLoader
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
import numpy as np 
import time

def normalizeArray(image, a=0, b=65535, dtype='uint16'):
    image_min = image.min()
    image_max = image.max()
    _max = (b - a) * (1.0/(image_max - image_min))
    _min = b - _max * image_max
    new = (_max * image + _min).astype(dtype)
    return new

print_info = lambda name, image, dt: print(name, image.dtype, np.min(image), np.max(image), dt)

src_c = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et2w_tse_clear_coronal.nii.gz"
src_s = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et1w_se_clear_sagital.nii.gz"
src_a = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et1w_se_clear_axial.nii.gz"

imageSagital = ImageLoader(src_s).load_array()[:,:,5]
imageCoronal = ImageLoader(src_c).load_array()[:,5,:]
imageAxial = ImageLoader(src_a).load_array()[5,:,:]
print("First")
print("Sag: ", imageSagital.shape, imageSagital.dtype, np.min(imageSagital), np.max(imageSagital))
print("Cor: ", imageCoronal.shape, imageCoronal.dtype, np.min(imageCoronal), np.max(imageCoronal))
print("Ax : ", imageAxial.shape, imageAxial.dtype, np.min(imageAxial), np.max(imageAxial))
print()
# imageAxial = cv2.normalize(imageAxial, None, 255,0, cv2.NORM_MINMAX, cv2.CV_8UC1)
t0 = time.time()
imageCoronal1 = cv2.normalize(imageCoronal, None, 65535,0, cv2.NORM_MINMAX, cv2.CV_16UC1)
t1 = time.time()
imageCoronal2 = normalizeArray(imageCoronal, 0 , 65535, 'uint16')
t2 = time.time()
imageCoronal3 = np.clip(imageCoronal.astype('uint16'), 0, 65535)
t3 = time.time()
dt0 = t1 - t0 
dt1 = t2 - t1 
dt2 = t3 - t2

print("After")
print_info("cv2Normalize: ", imageCoronal1, dt0)
print_info("normalizeArray: ", imageCoronal2, dt1)
print_info("clip: ", imageCoronal3, dt2)
cv2.imshow("cv2Normalize", imageCoronal1)
cv2.imshow("normalizeArray", imageCoronal2)
cv2.imshow("Clip", imageCoronal3)
cv2.waitKey(0) 
  
#closing all open windows 
cv2.destroyAllWindows() 