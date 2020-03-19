from sharepoint_store import Sharepoint_Store as sp
import pandas as pd
import numpy as np 
import getpass



unit_info = (('GP_SN','0156T'),
             ('GP_WO','823485'),
             ('PT_SN','PT_SN'),
             ('PT_WO','PT_WO'),
             ('RGB_SN','RGB_SN'),
             ('RGB_WO','8123wo'),
             ('Customer','PCM'),
             ('GP_Model','T4501S'),
             ('RGB_PN','WCS-CED-1840'),
             ('GP_PN','WG-T4501S-G'),
             ('GP_Family','C50')
             )

sharepoint_dict = {'base_url': 'https://ethosenergygroup.sharepoint.com/',
                    'tenant': 'ethosenergygroup.onmicrosoft.com',
                    'redirect_url': 'https://github.com/vgrem/Office365-REST-Python-Client/',
                    'site_url': 'https://ethosenergygroup.sharepoint.com/sites/ALT-Eng-US/',
                    'list_title': 'Solar Test Data',
                    }

authentication_dict = {'username': '',
                        'password': ''}

def sharepoint_auth_request():
    ''' method to request the authentication variables for sharepoint and check the login 
    will keep requesting until a good login is made'''

    

    authentication_dict = authentication_details_request()

    share_store = sp(unit_info, authentication_dict, sharepoint_dict)

    while share_store.make_context() is False:

        #logger here recording failed auth username

        authentication_dict = authentication_details_request()

        share_store = sp(unit_info, authentication_dict, sharepoint_dict)
    



def authentication_details_request():

    authentication_dict['username'] = input('Please input your username:       ')

    authentication_dict['password'] = getpass.getpass()

    return authentication_dict

#bulk_data = pd.read_csv("bulk_data.csv")
#input_data = pd.read_csv("InputSCT.txt", header=None, sep='\t')

#save_class = ds.Data_Store(bulk_data, input_data, unit_info, "C:/Users/robert.nelson/Documents/Technical Support/116 Test cell performance program/data_fetch")


sharepoint_auth_request()

share_store = sp(unit_info, authentication_dict, sharepoint_dict)

auth_check = share_store.make_context()

print(share_store.context.auth_context.provider.error)


del share_store


authentication_dict = {'username': 'robert.nelson@ethosenergygroup.com',
                        'password': 'M@ndymoon8'}

share_store = sp(unit_info, authentication_dict, sharepoint_dict)

auth_check = share_store.make_context()

print(share_store.context.auth_context.provider.error)

path = "2019_10_08_1133_824397_5018C_FLEET_T4501S.csv"

file_name = "2019_10_08_1133_824397_5018C_FLEET_T4501S.csv"

data_type = "Clean data"


share_store.upload_file(path, path, data_type, "3.6b")

del share_store


