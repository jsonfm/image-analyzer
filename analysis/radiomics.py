from numpy.core.fromnumeric import shape
from radiomics import featureextractor
import SimpleITK as sitk


settings = {}
settings = {}
settings['binWidth'] = 25
settings['resampledPixelSpacing'] = None  # [3,3,3] is an example for defining resampling (voxels with size 3x3x3mm)
settings['interpolator'] = sitk.sitkBSpline
settings['correctMask'] = True
extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
extractor.addProvenance(provenance_on=False)

# Disable all classes except firstorder
extractor.disableAllFeatures()

extractor.enableFeaturesByName(firstorder=[])
extractor.enableFeaturesByName(shape=[])
extractor.enableFeaturesByName(glcm=[])


def extract_features(image=None, mask=None, label=None):
    """It returns a ordered dict with features.
    
    Args:
        image (Simple ITK image): 2D/3D image object
        mask (Simple ITK image): mask object
        label (int):
        extractor(Pyradiomics Features Extractor)
    Example: 
        extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
        features_dict = extract_features(image, mask, label, extractor)
    """
    if extractor is None: raise('Extractor is None, please check it!')
    features = extractor.execute(image, mask, label)
    return features


def extract_features_series(images=None, masks=None):
    """ It returns features list from datasets of images and masks.
    Args:
        images (Dataset): 3D images dataset
        masks (Dataset): 3D masks dataset
        extractor(Pyradiomics features extractor)
    """
    if len(images) != len(masks): 
        raise('Images dataset must have same Len than masks dataset!')

    features_series = []

    for i in range(len(images)):
        image, mask = images[i], masks[i]
        features = extract_features(image, mask)
        features_series.append(features)

    return features_series

