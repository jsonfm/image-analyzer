from .radiomics import extract_features
import SimpleITK as sitk
import numpy as np


def merge_images_axis(axial, sagital, coronal):
    merged = [axial, sagital, coronal]
    return merged


def copy_metadata(image_1, image_2):
    """It copies medatada from one sitk image to another."""
    for k in image_1.GetMetaDataKeys():
        v = image_1.GetMetaData(k)
        image_2.SetMetaData(k, v)

    image_2.SetOrigin(image_1.GetOrigin())
    image_2.SetDirection(image_1.GetDirection())
    image_2.SetSpacing(image_1.GetSpacing())


def separate_hippocampus_mask(image_sitk, split_per=0.5, to_sitk=True):
    """It splits an sitk image on two sitk images or arrays."""
    mask = sitk.GetArrayFromImage(image_sitk)
    left_mask = np.zeros(mask.shape)
    right_mask = np.zeros(mask.shape)

    # Calculate percentage of each slice
    lim_1 = int(split_per*mask.shape[0])
    lim_2 = int(split_per*mask.shape[2])

    # Split image
    left_mask[:, :, :lim_2] = mask[:, :, :lim_2]
    right_mask[:, :, lim_2:] = mask[:, :, lim_2:]

    if to_sitk:
        left_mask = sitk.GetImageFromArray(left_mask)
        right_mask = sitk.GetImageFromArray(right_mask)
        copy_metadata(image_sitk, left_mask)
        copy_metadata(image_sitk, right_mask)

    return left_mask, right_mask


def to_array(image_sitk):
    """It transforms an sitk image to a numpy array."""
    return sitk.GetArrayFromImage(image_sitk)


def to_sitk(image_array):
    """It transforms and image array to sitk."""
    return sitk.GetImageFromArray(image_array)


def hippo_features(image, left_hippo, right_hippo, left_label=1, right_label=2):
    """It returns hippocampus features of each hemisphere."""
    features_left = extract_features(image, left_hippo, label=left_label)
    features_right = extract_features(image, right_hippo, label=right_label)
    return features_left, features_right


def asymmetry_index(volume_left, volume_right):
    """It calculates the asymetry index of volumes of hippocampus."""
    return 100*(volume_left - volume_right)/(volume_right + volume_left)


def print_features(features, id_space=50):
    """It prints nice the radiomic features."""
    for _id in features:
        print(f"{_id: <{id_space}} : {features[_id]}")
    print(f"----> Total Features: {len(features)}")
    print()


def right_left_features_vector(images, hippos):
    """It calculates features of a series of images and masks of hippocampus."""
    features_left_vector = []
    features_right_vector = []

    if len(images) < 0:
        raise(f'{images.name} series has not Images !')
    print()
    print("===> CALCULATING FEATURES")
    print(f"    -Images Series: {images.name}")
    print(f"    -Masks Series: {hippos.name}")
    print("--------------")
    print()
    for _id, _ in tqdm(images.items(), total=len(images), bar_format='{l_bar}{bar:20}{r_bar}{bar:-2b}'):
        # Read images
        image = images.get(_id, 0)
        hippo = hippos.get(_id, 0)

        # Separate in two slices hippocampus
        left_hippo, right_hippo = separate_hippocampus_mask(hippo)
        print(f"Current: {_id} , image size: {image.GetSize()}  , mask size {hippo.GetSize()}")
        # Calculate left and right hippocampus features
        features_left, features_right = hippo_features(image, left_hippo, right_hippo)

        features_left_vector.append(features_left)
        features_right_vector.append(features_right)
        print()
    print("===> COMPLETED!")
    return features_left_vector, features_right_vector


def calculate_and_save_features(images, hippos, left_name='left_hippo_data', right_name='right_hippo_data'):
    features_left_vector, features_right_vector = right_left_features_vector(images, hippos)
    left_hippo_data = pd.DataFrame(features_left_vector, index=images.keys())
    right_hippo_data =pd.DataFrame(features_right_vector, index=images.keys())

    if '.csv' not in left_name:
        left_name += '.csv'

    if '.csv' not in right_name:
        right_name += '.csv'
    
    left_hippo_data.to_csv(left_name)
    right_hippo_data.to_csv(right_name)