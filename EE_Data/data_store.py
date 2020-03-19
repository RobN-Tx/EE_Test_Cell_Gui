''' module/class to call to store the test report data '''
import pandas as pd
import numpy as np
from datetime import datetime
import os.path


class Data_Store:

    def __init__(self, raw_data, averaged_data, unit_info_tuples, root_storage_path):

        self.bulk_data = raw_data
        self.root_path = root_storage_path
        self.average_data = averaged_data
        self.unit_dict = dict(unit_info_tuples)
        self.date_string = self.make_date()
        self.unit_family = self.unit_dict['GP_Family']
        self.rgb_family = self.unit_dict['RGB_PN']
        self.gp_file_name = self.make_gp_filename()
        self.rgb_file_name = self.make_rgb_filename()
        self.bulk_gp_path = self.make_gp_bulk_path()

        # now check path exists
        self.folder_check(self.bulk_gp_path)

        self.clean_gp_path = self.make_gp_clean_path()
        # now check path exists
        self.folder_check(self.clean_gp_path)

        self.bulk_rgb_path = self.make_rgb_bulk_path()
        # now check path exists
        self.folder_check(self.bulk_rgb_path)

        self.clean_rgb_path = self.make_rgb_clean_path()
        # now check path exists
        self.folder_check(self.clean_rgb_path)

        #self.save_files()

        for item in self.unit_dict:
            print(item, self.unit_dict[item])

    def make_gp_bulk_path(self):
        '''method to make the bulk file local storage path'''

        bulk_path = os.path.join(self.root_path, 'bulk',  self.unit_family)

        return bulk_path

    def make_gp_clean_path(self):
        '''method to make the clean file local storage path'''

        clean_path = os.path.join(self.root_path, 'clean',  self.unit_family)

        return clean_path

    def make_rgb_bulk_path(self):
        '''method to make the bulk file local storage path'''

        bulk_path = os.path.join(self.root_path, 'bulk',  self.rgb_family)

        return bulk_path

    def make_rgb_clean_path(self):
        '''method to make the clean file local storage path'''

        clean_path = os.path.join(self.root_path, 'clean',  self.rgb_family)

        return clean_path

    def folder_check(self, check_path):
        '''method to check if a local folder exists
        if it doesnt make it'''

        if not os.path.exists(check_path):
            print(check_path)
            os.makedirs(check_path)

    def make_gp_filename(self):
        '''method to make the gp filename
        file name will be:
            Date
            GP_WO
            GP_SN
            Customer
            '''
        ud = self.unit_dict

        built_name = self.date_string + "_" + \
            ud['GP_WO'] + "_" + ud['GP_SN'] + "_" + \
            ud['Customer'] + "_" + ud['GP_Model']

        return built_name

    def make_date(self):
        now = datetime.now()

        return now.strftime("%Y_%m_%d_%H%M")

    def make_rgb_filename(self):
        '''method to make the rgb file name
        file name  will be:
            Date
            RGB_WO
            RGB_SN
            Customer
            '''
        ud = self.unit_dict

        built_name = self.date_string + "_" + \
            ud['RGB_WO'] + "_" + ud['RGB_SN'] + "_" + \
            ud['Customer'] + "_" + ud['RGB_PN']

        return built_name

    def save_files(self):
        '''method to save the supplied df to csv in the supplied path'''
        '''may need a different one depending on tag name storage'''
        tag_names = self.average_data[0]
        length = self.bulk_data.index.stop
        tag_names = tag_names[0:length]
        self.bulk_data = self.bulk_data.set_index(tag_names)

        print("saving files locally - ", self.date_string)
        gp_bulk_file_path = os.path.join(
            self.bulk_gp_path, self.gp_file_name) + ".csv"
        self.bulk_data.to_csv(gp_bulk_file_path, header=False)

        gp_clean_file_path = os.path.join(
            self.clean_gp_path, self.gp_file_name) + ".csv"
        self.average_data.to_csv(gp_clean_file_path, index=False, header=False)

        rgb_bulk_file_path = os.path.join(
            self.bulk_rgb_path, self.rgb_file_name) + ".csv"
        self.bulk_data.to_csv(rgb_bulk_file_path, header=False)

        rgb_clean_file_path = os.path.join(
            self.clean_rgb_path, self.rgb_file_name) + ".csv"
        self.average_data.to_csv(
            rgb_clean_file_path, index=False, header=False)

        return {"bulk_file": gp_bulk_file_path, "clean_file": gp_clean_file_path}
            
        

    def make_turbine_family(self):
        '''method to work out what turbine family this is:
            S10, S20, C40, C50, T60, M90, M100'''

        if self.unit_dict['GP_Model'].endswith('S'):
            unit_type = int(self.unit_dict['GP_Model'][1:-1])
        else:
            unit_type = int(self.unit_dict['GP_Model'][1:0])

        if unit_type < 1250:
            family = 'S10'

        elif 1260 < unit_type < 2000:
            family = 'S20'

        elif 2950 < unit_type < 4750:
            family = 'C40'

        elif 5450 < unit_type < 6250:
            family = 'C50'

        elif 6950 < unit_type < 7950:
            family = 'T60'

        elif 10000 < unit_type < 13050:
            family = 'M90'

        elif 13950 < unit_type < 16050:
            family = 'M100'

        else:
            family = 'unknown'
        print(family)
        return family
