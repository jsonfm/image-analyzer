from torch.utils.data import random_split
from torch import Generator
import nibabel as nib
import numpy as np


def split_dataset(dataset=None, to_train=0.75, seed=42):
    """Apply a random split to a dataset.

    Args:
        dataset (Dataset): some dataset
        to_train (float): percentage to train
        seed (int): Random split seed

    Returns:
        (train_dataset, test_dataset)

    """
    if dataset is None:
        raise('Dataset is None Type, check it please!')

    if 0 < to_train < 1:
        dataset_len = len(dataset)
        train_len = int(to_train*dataset_len)
        test_len = dataset_len - train_len

        train_dataset, test_dataset = random_split(dataset, [train_len, test_len], generator=Generator().manual_seed(seed))
        return train_dataset, test_dataset
    else:
        raise('Error: to_train must be > 0 and < 1 !')


def nii_load(image_path:str, dtype=np.float32):
    """It returns an image array given a path."""
    image_nii = nib.load(image_path, mmap=False)
    image_array = image_nii.get_fdata(dtype=dtype)
    # affine = image_nii.affine
    return image_array
