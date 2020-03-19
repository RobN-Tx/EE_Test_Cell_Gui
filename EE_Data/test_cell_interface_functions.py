'''module to hold the functions used for the ewon esque clx interface '''
import csv
import datetime
import logging
import os
import platform  # For getting the operating system name
import shutil
import subprocess  # For executing a shell command

#import ee_interface_config as cfg 
from EE_Data.eip import PLC

#import clx_interface_functions as clx

functions_logger = logging.getLogger("test_cell_logger.functions")



def send_data(data_file_name):
    '''function to write data to file'''
    print("send data")



def file_archiver(file_name, folder_name):
    '''function to rename the exisiting file and store in an archive folder
    future dev - clear archive folder after xx days'''

    # make time stamp string:
    now = datetime.datetime.utcnow()

    time_string = now.strftime('%d-%m-%Y %H-%M ')

    shutil.move(file_name, folder_name + '/' + time_string+file_name)
    # print("moved")





def folder_make():
    """ function to build the folders required for data storage if they dont exist

    Usage:: called at the start of the script, to check if the archive and store folders exist

    param: none
    """

    current_directory = os.getcwd()
    # print(current_directory)
    folder1 = os.path.join(current_directory, r'archive')
    folder2 = os.path.join(current_directory, r'store')
    if not os.path.exists(folder1):
        print("path doesn't exist. trying to make")
        os.makedirs(folder1)
    if not os.path.exists(folder2):
        print("path doesn't exist. trying to make")
        os.makedirs(folder2)





