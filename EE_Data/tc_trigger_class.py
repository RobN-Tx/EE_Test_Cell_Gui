'''Class for the Ethos Energy Light Turbines LLC test cell performance program automation'''

import configparser
import csv
import datetime
import logging
import os
import platform  # For getting the operating system name
import shutil
import subprocess  # For executing a shell command
import json
import pandas as pd
import numpy as np
import win32com.client as com   #Make sure  you have this module installed - pip install pywin32
import getpass

from EE_Data.data_store import Data_Store as ds
from EE_Data.sharepoint_store import Sharepoint_Store as sp

from EE_Data.eip import PLC

module_logger = logging.getLogger("test_cell_logger.trigger")

import pythoncom
import win32com



#####################
# TODO:
# 1. Improve the authenication storage method - done!
# 2. Add error catching for the sharepoint storage
# 3. not sure...

class Gather_Class:
    ''' The class used for gathering and sorting out the test cell performance data'''

    def __init__(self, config_data, testing_mode=False):

        # setup the logger
        self.logger = logging.getLogger('test_cell_logger.trigger.Trigger_Check')
        self.logger.info('creating an instance of Trigger_Check')

        # load the config settings from the config data that was passed for the data gather and trigger
        self.trigger_tag = config_data['trigger_tag']
        self.testing = testing_mode
        self.number_of_pulls = int(config_data['number_of_pulls'])
        self.data_tag_names = config_data['data_tag_names']
        self.data_tag_list = config_data['data_tag_list']
        self.string_tag_list = config_data['string_tag_list']
        self.string_tag_names = config_data['string_tag_names']
        self.slice_size = int(config_data['tag_list_slice_size'])
        self.unit_type_dict = config_data['unit_type_dict']
        self.unit_type_tag = config_data['unit_type_tag']
        self.solonox_tag = config_data['solonox_tag']
        self.mc_directory = config_data['mc_dir']
        self.single_shaft_script_file = config_data['single_shaft_script_file']
        self.twin_shaft_script_file = config_data['twin_shaft_script_file']
        self.store_path = config_data['storage_dir']
        self.version = config_data['version']
        #self.unit_type_dict = json.loads(self.unit_type_dict)
        self.output_data = ()
        self.data_tag_slices = None


        # sharepoint config kit - for storing the files in sharepoint

        self.sharepoint_dict = config_data['sharepoint_dict']
        #self.sharepoint_dict = json.loads(self.sharepoint_dict)

        self.external_storage_files = config_data['paths_to_other_files_to_store_dict']
        #self.external_storage_files = json.loads(self.external_storage_files)

        #define the authentication dictionary
        self.authentication_dict = config_data['authentication_dict']
                
        #setup the sharepoint auth details and check them
        #self. sharepoint_auth_request()

        #setup the PLC connection
        self.comm = PLC()
        self.comm.IPAddress = config_data['ip_address']
        self.comm.ProcessorSlot = int(config_data['slot_number'])

        #call the tag slicer and setup the tag list for the reads
        self.tag_slicer()

    def sharepoint_auth_request(self, passed_auth_dict):
        ''' method to request the authentication variables for sharepoint and check the login 
        will keep requesting until a good login is made'''

        #self.authentication_details_request()

        if len(passed_auth_dict['username'].split("@")) < 2:
            passed_auth_dict['username'] = passed_auth_dict['username'] + "@ethosenergygroup.com"

        #blank unit info for the start up check of authentication
        unit_info = {}

        share_store = sp(unit_info, passed_auth_dict, self.sharepoint_dict)

        #while share_store.make_context() is False:

            #logger here recording failed auth username

        #    self.authentication_details_request()

        #    share_store = sp(unit_info, self.authentication_dict, self.sharepoint_dict)\

        if share_store.make_context():

            self.authentication_dict = passed_auth_dict
        
        return share_store.make_context()

    def authentication_details_request(self):

        self.authentication_dict['username'] = input('Please input your username:       ')

        if len(self.authentication_dict['username'].split("@")) < 2:
            self.authentication_dict['username'] = self.authentication_dict['username'] + "@ethosenergygroup.com"
            
        self.authentication_dict['password'] = getpass.getpass()

    def trigger_read(self):      
        '''method to read the trigger tag
            if trigger tag is true - then run the data fetch code
            if tag is false and the testing flag in config is 1 '''


        ask = '0'

        try:
            plc_trigger_value = self.comm.Read(self.trigger_tag)
                           
            if self.testing is True:
                ask = input("enter 1 to test")
                
        except:
            
            print("trigger fails")
            plc_trigger_value = False
            self.logger.error("Trigger read failed", exc_info=True)
   
        if plc_trigger_value is True or ask is '1':
            trigger_value = True
        
        else:
            trigger_value = False


        return trigger_value

    def run_performance_test(self):


            self.data_fetch()
            self.data_processing()
            self.save_data()

            if self.testing:
                
                self.store_data()
                self.call_mc()

            else:

                store_flag = self.call_mc()

                
                self.store_data()

    def data_fetch(self):
        '''function to collect as many data sampels as defined in the config'''

        
        data_frame = pd.DataFrame()
        column = 0
        while column < self.number_of_pulls:
            data_frame[column] = self.data_read()
            #print(data_frame)
            column = column  + 1
        self.bulk_data = data_frame
        
    def data_processing(self):
        ''' process the data to remove outliers and then average the data and output'''

        #store the bulk data
        self.bulk_data.to_csv("bulk_data.csv", index=False)
        mean = list(self.bulk_data.mean(axis=1))


        now = datetime.datetime.now()
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%I:%M %p")
        output = [date, time]
        
        self.output_data = mean + output
        

        #z_data = np.abs(stats.zscore(self.bulk_data))
        #pd.DataFrame(z_data).to_csv("Z_Data.csv", index=False,)
        #print(z_data)
        #print("wait")
        #print(np.where(z_data >3))

    def string_data_fetch(self):
        ''' method to fetch the string data and store in self
        called every time before saving data to csv'''
        string_data = []
        try:
            

            for index, tag in enumerate(self.string_tag_list):
                print(tag)
                print(index)

                string_tag_data = self.comm.Read(tag)

                string_tag_data = str(string_tag_data).replace('/','-').replace("\\",'-')

                if string_tag_data == 'NA':
                    string_tag_data = "000000"

                string_tuple = (self.string_tag_names[index], string_tag_data)

                print(string_tuple)
                string_data.append(string_tuple)

                

            GP_Model_Tuple = self.unit_type_finder()
            string_data.append(GP_Model_Tuple)

            string_data.append(self.make_turbine_family(GP_Model_Tuple))


        
        except:
            #good_data_flag = False
            self.logger.error('failed on this PLC on these tags %s', tag)
            print(self.string_tag_list)
            print("fail.com")
            #failed_plc = unit_info['ip_address']
        return string_data

    def save_data(self):
        '''method to save the data, both numerical and string
        to a pre defcsv - defined in .ini file '''
         
        self.string_data = self.string_data_fetch()
        self.data_tag_names = self.data_tag_names + ["Date", "Time"]
        final_dataFrame = pd.DataFrame(list(zip(self.data_tag_names, self.output_data)))
        final_dataFrame = final_dataFrame.append(self.string_data, ignore_index = True)


        final_dataFrame.to_csv(self.mc_directory+"InputSCT.txt", index=False, header=False, sep="\t")
        self.final_dataFrame = final_dataFrame

    def store_data(self):
        # new storage logic, new class, create then destroy?!
        
        #store the files locally:
        #string_data = self.string_data_fetch()
        #final_dataFrame = pd.DataFrame(list(zip(self.data_tag_names, self.output_data)))
        #final_dataFrame = final_dataFrame.append(string_data, ignore_index = True)

        try: 
            storage_routine = ds(self.bulk_data, self.final_dataFrame, self.string_data, self.store_path)

            self.file_paths = storage_routine.save_files()

                
            print(self.file_paths)

        except:
            
            print("trigger fails")
            self.logger.error("Local store failed", exc_info=True)

        del storage_routine

        sharepoint_storage = sp(self.string_data, self.authentication_dict, self.sharepoint_dict)

        sharepoint_storage.make_context()

        sharepoint_storage.upload_file(self.file_paths["bulk_file"],os.path.basename(self.file_paths["bulk_file"]), "Bulk Data", self.version)

        sharepoint_storage.upload_file(self.file_paths["clean_file"],os.path.basename(self.file_paths["clean_file"]), "Clean Data", self.version)

        sharepoint_storage.upload_file(self.mc_directory+"InputSCT.txt",os.path.basename(self.file_paths["clean_file"]), "Input File", self.version)


        for file in self.external_storage_files:

            file_name = os.path.basename(self.file_paths["clean_file"])

            file_path = self.external_storage_files[file]
            file_type = file

            sharepoint_storage.upload_file(file_path, file_name, file_type, self.version)



        

        del sharepoint_storage

    def call_mc(self):
        #method to call model center

        try:
            mc = com.Dispatch('Phoenix.Modelcenter')

            if self.isSingleShaft():
                script_file_to_use = self.single_shaft_script_file
            else:
                script_file_to_use = self.twin_shaft_script_file

            print(script_file_to_use)

            mc.loadModel(os.path.join(self.mc_directory, script_file_to_use)) 

            print("running script")
            mc_return = mc.run("")
            print("MC return complete")

            return_variable = True

        except:
            
            print("model center fails")
            print(mc_return)
            self.logger.error("Model center failed", exc_info=True)
            return_variable = False

        return return_variable
        
    def isSingleShaft(self):

        '''method to find out if it is single or twin shaft
        if it is single it will return true.
        if twin it will return false'''
        
        if self.report_unit_string.endswith('S'):
            string_type = self.report_unit_string[1:-1]

        else:
            string_type = self.report_unit_string[1:]
        
        isSingleShaft = string_type.endswith('1')

        return isSingleShaft
        
    def data_read(self):
        #print("data_read")
        data = []
        try:
            #with PLC() as comm:

                # initial a PLC interface, set it to the config files IP address
                #comm = PLC()
                #comm.IPAddress = unit_info['ip_address']

            for tags in self.data_tag_slices:
                # print(len(tags))
                # fetch the values of the tags from the above PLC
                #print(tags)
                # print(len(tags))
                if len(tags) > 1:
                    value = self.comm.Read(tags)
                    #print(value)
                else:
                    value = [self.comm.Read(tags[0])]
                    #print(value)
                # print(len(value))
                data = data + value
                    # print(data)
            # completeion_time = int(
                # datetime.datetime.utcnow().timestamp()) - time_data['time_int']

            # app_log_string = app_log_string+"Unit " + \
                #str(unit_id) + " - " + str(completeion_time) + ", "
        except:
            #good_data_flag = False
            self.logger.error('failed on this PLC on these tags %s', tags)
            print(tags)
            print("fail.com")
            #failed_plc = unit_info['ip_address']
        return data

    def tag_slicer(self):
        '''Method to take the list of tags, slice into 
        config['tag_list_slice_size'] pieces and store in the
        object instance as data_tag_slices'''

        tag_slices = []
        #range(start, stop, step)
        for i in range(0, len(self.data_tag_list), self.slice_size):
            chunk = self.data_tag_list[i:i + self.slice_size]
            # print(chunk)
            tag_slices.append(chunk)

        self.data_tag_slices = tag_slices

    def unit_type_finder(self):
        '''function to fetch the current unit under test id # and also the solonox flag
        then build and return the unit type for the performance and the unit type plus solonox flag for the report'''

        unit_id_no = self.comm.Read(self.unit_type_tag)
        solonox_flag = self.comm.Read(self.solonox_tag)

        self.unit_id_string = "T" + self.unit_type_dict[str(unit_id_no)]

        print(self.unit_id_string)

        if solonox_flag is True:
            self.report_unit_string = self.unit_id_string + "S"
        else:
            print("not solonox")
            self.report_unit_string = self.unit_id_string

        unit_tuple = ('GP_Model', self.report_unit_string)

        return unit_tuple
        #self.report_unit_string = 

    def make_turbine_family(self, GP_Model_Tuple):
        '''method to work out what turbine family this is:
            S10, S20, C40, C50, T60, M90, M100'''
        GP_Model = GP_Model_Tuple[1]
        print(GP_Model)
        if GP_Model.endswith('S'):
            #unit_type = int(GP_Model[1:-1])
            string_type = GP_Model[1:-1]
            unit_type = int(string_type)

        else:
            string_type = GP_Model[1:]
            unit_type = int(string_type)

        if unit_type < 1350:
            family = 'S10'

        elif 1360 < unit_type < 2000:
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
        return ("GP_Family", family)

        
