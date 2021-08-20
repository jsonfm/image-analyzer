import numpy as np


def calculate_volume(image, dx:float=1.0, dy:float=1.0, dz:float=1.0):
    """Calculate volume of a 3d image array.
    Args:
        image (numpy array): image array
        dx(float): voxel spacing on X axis mm3
        dy(float): voxel spacing on Y axis mm3
        dz(float): voxel spacing on Z axis mm3

    """
    dv = dx*dy*dz
    fxyz_sum = np.sum(image != 0)
    volume = fxyz_sum * dv
    return volume


def calculate_volume_series(images=None, dx:float=1.0, dy:float=1.0, dz:float=1.0):
    """It returns a list of calculated volumes from a list of 3D images."""
    volumes = [calculate_volume(image, dx, dy, dz) for image in images]
    return volumes


def get_roi3d(img, mask):
    """It returns a 3D region of interest (ROI) of a image 3D starting from a mask.
    
    Args:
        img (array - 3d): image
        mask(array - 3d): mask
    """
    roi3d = np.zeros(img.shape)
    roi3d[mask > 0] = img[mask > 0]
    return roi3d
