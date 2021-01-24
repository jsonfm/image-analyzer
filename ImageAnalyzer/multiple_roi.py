from pencil_roi import PencilROI


class MultipleROI(object):
    def __init__(self, roi_prefix="ROI "):
        self.slices = {}
        self.index = {}
        self.prefix = roi_prefix

    def __getitem__(self, item):
        return self.slices

    def __setitem__(self, key, value):
        self.slices[key] = value

    def __len__(self):
        return len(self.slices)

    def addNewROI(self, slice_name="Slice 1", roi_name=None):
        """It create a new ROI object
        :param slice_name
        :param roi_name
        """
        if slice_name not in self.index:
            self.index[slice_name] = 1
        else:
            self.index[slice_name] += 1

        if roi_name is None:
            roi_name = self.prefix + str(self.index[slice_name])

        if slice_name not in self.slices:
            self.slices[slice_name] = {}
            self.slices[slice_name][roi_name] = PencilROI(ID=roi_name)
        else:
            self.slices[slice_name][roi_name] = PencilROI(ID=roi_name)

    def rename(self, name=None, slice_name=None, old_key=None, new_key=None):
        """It renames a ROI
        :param name:
        :param slice_name:
        :param old_key:
        :param new_key:

        Usage:
        rename(name="Slice 1, ROI 1", new_key="Heart")
        rename(slice_name="Slice 1", old_key="ROI 1", new_key="Heart")
        """
        if name:
            print("deleting NAME: ", name)
            slice_name, old_key = self.readComposedNames(name)

        if slice_name and old_key and new_key:
            if old_key != new_key:
                if old_key in self.slices[slice_name]:
                    self.slices[slice_name][new_key] = self.slices[slice_name][old_key]
                    self.slices[slice_name][new_key].ID = new_key
                    self.slices[slice_name].pop(old_key)
                else:
                    raise Exception(old_key + " doesn't exist in ROIs list. Please Check it and retry!")
        else:
            raise Exception("Cannot found elements to delete...")

    def deleteROI(self, name=None, slice_name=None, roi_name=None):
        """It deletes elements from the dict
        :param name: composed name like "Slice 1 , ROI 1"
        :param slice_name: for example "Slice 1"
        :param roi_name: for example "ROI 1"
        """
        if slice_name and roi_name:
            self.slices[slice_name].pop(roi_name)
            return

        if slice_name:
            self.slices.pop(slice_name)
            return

        if name:
            slice_name, roi_name = self.readComposedNames(name)
            self.slices[slice_name].pop(roi_name)
            self.index[slice_name] -= 1
            return

    def clear(self):
        self.slices = {}
        self.index = {}

    def prettyPrint(self):
        print("-----------------------------------------")
        for _slice in self.slices:
            print(_slice)
            for roi in self.slices[_slice]:
                print("  -", roi)
        print("-----------------------------------------")

    @staticmethod
    def readComposedNames(name):
        names = name.split(",")
        if names[0][-1] == " ":
            names[0] = names[0][:-1]
        if names[1][0] == " ":
            names[1] = names[1][1:]
        slice_name = names[0]
        roi_name = names[1]
        return slice_name, roi_name

    def getROI(self, name=None, slice_name=None, roi_name=None):
        """It returns the corresponding ROI
        :param name: composed name like "Slice 1 , ROI 1"
        :param slice_name: for example "Slice 1"
        :param roi_name: for example "ROI 1"
        """
        if slice_name and roi_name:
            if slice_name in self.slices and roi_name in self.slices[slice_name]:
                return self.slices[slice_name][roi_name]

        if name:
            slice_name, roi_name = self.readComposedNames(name)
            if slice_name in self.slices and roi_name in self.slices[slice_name]:
                return self.slices[slice_name][roi_name]

        return None

    def getNamesList(self):
        names_list = []
        for _slice in self.slices:
            for roi in self.slices[_slice]:
                name = _slice + " , " + roi
                names_list.append(name)
        return sorted(names_list)

    def obtainVolume(self):
        pass
# s = MutipleROI()
# s.addNewROI("Slice 1")
# s.addNewROI("Slice 1")
# s.addNewROI("Slice 2")
# s.addNewROI("Slice 3")
# s.rename(name="Slice 1 , ROI 1", new_key="Higado")
#
# s.prettyPrint()
# l = s.getNamesList()
