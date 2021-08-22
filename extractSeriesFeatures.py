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