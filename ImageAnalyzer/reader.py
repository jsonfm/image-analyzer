import os

class ImageReader(object):
    def __int__(self):
        self.root = None
        self.seriesList = None

    def load_images_series(self):
        pass

    def load_dicom_series(self, path):
        for root, _ , files in os.walk(path):
            self.root = root
            self.seriesList.addItems(sorted(files))

    def read_dicom_image(self):
        pass

    def array_to_pixmap(self):
        pass

    def linear_convert(self):
        pass