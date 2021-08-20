import os
from numpy.lib.shape_base import split 
import pydicom
import time
import pandas as pd 
# Mejorar el rendimiento de este algoritmo

def clean_text(string):
    # clean and standardize text descriptions, which makes searching files easier
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_") # replace everything with an underscore
    return string.lower()  

def anonymize(data):
    data.PatientName = "anonymus" 

def order_file(filename:str, dst:str, patient_prefix="Patient"):
    
    ds = pydicom.read_file(os.path.join(filename), force=True)
    
    # Anonymize data
    anonymize(ds)
    
    # Read metadata
    patientID = clean_text(ds.get("PatientID", "NA"))
    studyDate = clean_text(ds.get("StudyDate", "NA"))
    studyDescription = clean_text(ds.get("StudyDescription", "NA"))
    seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))
    modality = ds.get("Modality","NA")
    seriesInstanceUID = ds.get("SeriesInstanceUID","NA")
    instanceNumber = str(ds.get("InstanceNumber","0"))   
    
    # Folder format
    patient_name = f"{patient_prefix} - {patientID}"
    patient_folder = os.path.join(dst, patient_name) # Patient xxxx
    study_folder = os.path.join(patient_folder, studyDescription) # encefalo
    serie_folder = os.path.join(study_folder, seriesDescription) # t1_axial
    
    if not os.path.exists(patient_folder):
        os.mkdir(patient_folder)

    if not os.path.exists(study_folder):
        os.mkdir(study_folder)

    if not os.path.exists(serie_folder):
        os.mkdir(serie_folder)
    
    image_name = f"{modality} - {instanceNumber}.dcm"
    full_name = os.path.join(serie_folder, image_name)
    ds.save_as(full_name)


def order_series(src, dst):
    i = 0
    for root, dirs, files in os.walk(src):
        if root != src:
            for file in files:
                if ".dcm" in file:
                    filename = os.path.join(root, file)
                    order_file(filename, dst)


def get_patients_ids(src):
    """It returns ad dict composed by the patients name and their patients' id.
    Returns:
        {
        patient_name_1 : patient_id_1
        patient_name_2 : patient_id_2
        patient_name_3 : patient_id_3
                    *
                    *
                    *
        }
    """
    ids = {}
    last_patient = ""
    for root, dirs, files in os.walk(src):
        if root != src:

            if len(dirs) > 0:
                patient_name = root.split("/")[-1]

            if len(files) > 3 and len(dirs) == 0 and last_patient != patient_name:              
                filename = files[2]
                filepath = os.path.join(root, filename)
                last_patient = patient_name
                ds = pydicom.read_file(filepath, force=True)
                patientID = clean_text(ds.get("PatientID", "NA"))
                ids[patient_name] = patientID
    return ids

def pretty_print_dict(title:str, _dict):
    print()
    print(f" ========================= {title.upper()} ========================")
    for _id in _dict:
        print(f"  -> {_id: <30} : {_dict[_id]}")
    print()
# Order dicom series ===================================================
# src = "/home/jason/Documents/TESIS/dataset-utpl-emt/otros/"
# dst = "/home/jason/Documents/TESIS/elt-analyzer/data/dataset-dicom/others/"
# t0 = time.time()
# order_series(src, dst)
# t1 = time.time()

# dt = t1 - t0
# print(f"Elapsed: {dt} secs.")


# Get Patients id =======================================================
# src_sclerosis = "/home/jason/Documents/TESIS/dataset-utpl-emt/esclerosis/"
# src_others = "/home/jason/Documents/TESIS/dataset-utpl-emt/otros"
# sclerosis_patients = get_patients_ids(src_sclerosis)
# others_patiens = get_patients_ids(src_others)

# pretty_print_dict("sclerosis patients", sclerosis_patients)
# pretty_print_dict("others patients", others_patiens)
# sclerosis = pd.DataFrame.from_dict(sclerosis_patients, orient="index")
# others = pd.DataFrame.from_dict(others_patiens, orient="index")
# sclerosis.to_csv('sclerosis.csv')
# others.to_csv('others.csv')


    
    