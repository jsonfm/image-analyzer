import numpy as np
import cv2 


def draw_mask_over_image(image, mask, alf=0.5):
    "Given an and image and a mask it will return a new image with the mask overlapping."
    painted = np.copy(image)
    painted[(mask == 255).all(-1)] = [0, 255, 0]
    new = cv2.addWeighted(painted, 1-alf, image, alf, 0, painted)
    return new


def get_binary_mask(mask):
    "It will return a binary a mask given a mask with float or int values."
    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)
    ret, mask = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)
    return mask