import os
import pydicom 
import dicom2nifti
import shutil

# base_path = "/home/jason/Documents/TESIS/TRAIN/"
# folders = os.listdir(base_path)
# for folder in folders:
#     dir_base = os.path.join(base_path, folder)
#     subfolders = os.listdir(dir_base)
#     if len(subfolders) < 2:
#         dir_s = os.path.join(base_path, dir_base, subfolders[0])
#         subs = os.listdir(dir_s)
#         if len(subs) > 2:
#             print(folder, " || Len: ", len(subs))
#         else: 
#             remove_dir = os.path.join(base_path, folder)
#             shutil.rmtree(remove_dir)
#             print("remove: ", remove_dir)

# f = os.path.join(base_path, dic[0])
# test = pydicom.dcmread(f)
# print(test)

#dicom2nifti.dicom_series_to_nifti(base_path, '708445 - sagital.nii', reorient_nifti=True)