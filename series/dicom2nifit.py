import os
import dicom2nifti


def transform_dicom_series(src, dst):
    i = 0
    n = 0
    last_patient = ""
    patient = ""
    total = len(os.listdir(src)) - 1
    for root, dirs, files in os.walk(src):
        _split = root.split('/')
        #print(root, len(_split))
        if root != src:
            for serie_name in dirs:
               if len(_split)>10: 
               
                    study = _split[-1]
                    patient = _split[-2]
                    full_serie_name = os.path.join(root, serie_name)
                    nifti_name = f"{serie_name}.nii"
                    patient_folder = os.path.join(dst, patient)
                    study_folder = os.path.join(patient_folder, study)
                    full_nifti_name = os.path.join(study_folder, nifti_name)

                    if not os.path.exists(patient_folder):
                        os.mkdir(patient_folder)
                    if not os.path.exists(study_folder):
                        os.mkdir(study_folder)
                    try:                
                        dicom2nifti.dicom_series_to_nifti(full_serie_name, output_file=full_nifti_name, reorient_nifti=True)
                    except Exception as e:
                        print(e)
                    # print(study, patient)
                    # print(full_serie_name)
                    # print(full_nifti_name)
                    # print("--------------")

src = "/home/jason/Documents/TESIS/elt-analyzer/data/dataset-dicom/others/"
dst = "/home/jason/Documents/TESIS/elt-analyzer/data/dataset-nifti/others/"
transform_dicom_series(src, dst)
# dicom2nifti.dicom_series_to_nifti(src, dst, reorient_nifti=True)