import os
import re
import SimpleITK as sitk
from analysis.radiomics import extract_features


def load_sitk(src):
    return sitk.ReadImage(src)

def load_array(src):
    return sitk.GetArrayFromImage(load_sitk(src))

class ImageLoader:
    """It load an image on .nii or .nii.gz format.
    
    Args:
        src (str): image directory
    
    Example:
        img = ImageLoader(src)
        img_sitk = img.load()
        img_array = img.load_array()
    """
    def __init__(self, src:str, _id:str=""):
        self.src = src
        self.id = _id

    def load_sitk(self):
        """It returns a sitk image loaded with the src."""
        return sitk.ReadImage(self.src)

    def load_array(self):
        """It returns a numpy array of loaded with the src."""
        return sitk.GetArrayFromImage(self.load_sitk())
    
    def get(self):
        return self.load_array()








