import EE_Data.data_store as ds
import pandas as pd
import numpy as np 


unit_info = (('GP_SN','0156T'),
             ('GP_WO','823485'),
             ('PT_SN','PT_SN'),
             ('PT_WO','PT_WO'),
             ('RGB_SN','RGB_SN'),
             ('RGB_WO','8123wo'),
             ('Customer','PCM'),
             ('GP_Model','T4501S'),
             ('RGB_PN','WCS-CED-1840'),
             ('GP_Family', 'C55')
             )

bulk_data = pd.read_csv("bulk_data.csv")
input_data = pd.read_csv("InputSCT.txt", header=None, sep='\t')

save_class = ds.Data_Store(bulk_data, input_data, unit_info, "C:/Users/robert.nelson/Documents/Technical Support/116 Test cell performance program/data_fetch")

#
#