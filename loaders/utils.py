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

