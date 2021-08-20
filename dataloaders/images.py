import os
import re
import SimpleITK as sitk
from analysis.radiomics import extract_features


def search_in_1(lst:list, filters:list):
    results = []
    for filt in filters:
        for element in lst:
            if filt in element:
                if element not in results:
                    results.append(element)
    return results


def search_in_2(lst:list, filters:list):
    filter_func = lambda key, lst: [element for element in lst if re.search(key, element)]
    results = []
    for filt in filters:
        results += filter_func(filt, lst)
    return set(results)



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


class NIISeries:
    """It loads multiples series of images on dict of series
    Example:
        images = NIISeries(src, filters=['t1','sagital'], include_with='hippo')

        print(images)
        # it will return a dict like this
        {
            'Patient - 1': [ImageLoader_0, ImageLoader_1, ImageLoader_2, ... ]
            'Patient - 2': [ImageLoader_0, ImageLoader_1, ImageLoader_2, ... ]
            'Patient - 3': [ImageLoader_0, ImageLoader_1, ImageLoader_2, ... ]
                                    .
                                    .
                                    .
        }
        # You could use:
        images.pretty_print()
    """
    def __init__(self, src:str, filters:None, include_with=None, name=None):
        if isinstance(filters, str):
            if len(filters) > 0: filters = [filters]
            else: filters = None

        if isinstance(filters, list):
            if len(filters) < 1: filters = None

        self.name = name
        self.filters = filters
        self.images = self.search_images_in(src, filters, include_with)

    def __iter__(self):
        return iter(self.images)

    def __getitem__(self, key):
        return self.images[key]

    def __len__(self):
        return len(self.images)
    
    def keys(self):
        return self.images.keys()
    
    def items(self):
        return self.images.items()
    
    def get(self, _id:str, indx:int, to_sitk=True):
        """It returns a specific element of the series."""
        if to_sitk:
            return self.images[_id][indx].load_sitk()
        else:
            return self.images[_id][indx].load_array()

    def search_filter(self, key:str, lst:list):
        """It searchs some coincidence on a list of strings given a key."""
        return [element for element in lst if re.search(key, element)]
    
    def check_file_formats(self, files):
        formats = ['nii', '.nii.gz']
        return search_in_1(files, formats)

    def filter_list(self, lst:list, filters:list, include_with=None, check_format=False):
        """It will filter a list with a list of filters (keywords)."""
        result = []
        include = True

        if check_format:
            lst = self.check_file_formats(lst)

        # Check include condiction
        if include_with is not None: 
            include = len(self.search_filter(include_with, lst)) > 0 

        # if include with is on list, add filtered files
        if include:
            result = search_in_1(lst, filters)

        return result

    def search_images_in(self, src:str, filters=None, include_with=None):
        """It will search images on """
        images = {}
        for root, dirs, files in os.walk(src):
            if len(dirs) == 0:                
                if filters is not None:
                    files = self.filter_list(files, filters, include_with)
                if len(files) >0:
                    _id = root.split('/')[-2]
                    images[_id] = [ImageLoader(os.path.join(root, file), file) for file in files]
        return images
    
    def pretty_print(self, max_elements=10, max_series=100):
        """It prints in a pretty format the current series."""
        current_element = 1
        current_serie = 1
        print("=========================== SERIES INFO ===========================")
        print()
        print(f"{'SERIES NAME: '.ljust(19)}{self.name}")
        print(f"{'NUMBER OF SERIES: '.ljust(16)} {len(self.images)}")
        print(f"{'FILTERS:'.ljust(22)} {self.filters}")
        print("--------")
        for _id in self.images:
            print()
            print(f"   * {_id}  |  files: {len(self.images[_id])}")
            print()
            for image in self.images[_id]:
                print(f"         -->  {image.id}")
                current_element += 1
                if current_element > max_elements:
                    for _ in range(3):
                        print("                  .")
                    break
            current_element = 0
            current_serie += 1
            if current_serie > max_series:
                print("")
                for _ in range(3):
                    print("                 ...")
                break
        print()


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


# src_sclerosis = "/home/jason/Documents/TESIS/elt-analyzer/data/dataset-nifti/sclerosis"
# src_others = "/home/jason/Documents/TESIS/elt-analyzer/data/dataset-nifti/others"

# t2_slcerosis_coronal = NIISeries(src_sclerosis, filters=['cor'], include_with='hippo', name="T2 Sclerosis Coronal")
# t2_hippos_sclerosis_coronal = NIISeries(src_sclerosis, filters=['hippo'], name='T2 Sclerosis Hippos')

# t2_others_coronal = NIISeries(src_others, filters=['cor'], include_with='hippo', name="T2 Others Coronal")
# t2_hippos_others_coronal = NIISeries(src_others, filters=['hippo'], name='T2 others Hippos')

# t2_slcerosis_coronal.pretty_print(max_elements=2, max_series=3)
# t2_hippos_sclerosis_coronal.pretty_print(max_elements=3, max_series=5)
# t2_others_coronal.pretty_print(max_elements=3, max_series=5)
# t2_hippos_others_coronal.pretty_print(max_elements=3, max_series=5)


# t1 = time.time()
# calculate_and_save_features(t2_slcerosis_coronal, t2_hippos_sclerosis_coronal, left_name='left_hippo_sclerosis_data', right_name='right_hippo_sclerosis_data')
# calculate_and_save_features(t2_others_coronal, t2_hippos_others_coronal, left_name='left_hippo_others_data', right_name='right_hippo_others_data')

# t2 = time.time()
# print(f"Elapsed: {t2 - t1} secs.")