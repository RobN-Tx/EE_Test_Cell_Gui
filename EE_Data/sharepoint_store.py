#
# sauce:
# https://github.com/vgrem/Office365-REST-Python-Client/blob/master/examples/sharepoint/file_operations.py
# 
import json
import os
#hi me
#from EE_Data.sharepoint_settings import settings

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.caml_query import CamlQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.file import File
from office365.sharepoint.file_creation_information import FileCreationInformation
from office365.sharepoint.list_data_service import ListDataService















class Sharepoint_Store:

    def __init__(self, unit_info_tuples, authentication_dict, sharepoint_info_dict):
        '''initialization method
        inputs:
        unit_info_tuples from the main tc class
        authentication dict - holds user and password, gotta confirm how to inputgather these
        sharepoint_inf_dict - holds the site url, tenant info, maybe target folder?
        '''
        self.site_url = sharepoint_info_dict['site_url']
        self.target_list_title = sharepoint_info_dict['list_title']
        self.authentication_dict = authentication_dict

        self.unit_dict = dict(unit_info_tuples)


        

        ###### DEV Vars

        
        ######
        

    
        

    def make_context(self):

        ctx_auth = AuthenticationContext(url=self.site_url)


        
        ctx_auth.acquire_token_for_user(username=self.authentication_dict['username'], password=self.authentication_dict['password'])
        #ctx_auth.acquire_token_for_user(username='robert.nelson@ethosenergygroup.com', password='M@ndymoon8') 
        self.context = ClientContext(self.site_url, ctx_auth)

        if self.context.auth_context.provider.error is not '':
            #the the login didnt work!
            returning_variable = False
        else:
            #the login worked!
            returning_variable = True
        
        return returning_variable
        
            

    def spare_method(self):
        print("hi")

    def upload_file(self, file_path, file_name, data_type, software_version):

        upload_into_library = True
        
        # rn_test_1.csv
        with open(file_path, 'rb') as content_file:
            file_content = content_file.read()

        if upload_into_library:
            list_title = "Solar Test Data"
            target_folder = self.context.web.lists.get_by_title(list_title).root_folder


            file_extension = os.path.basename(file_path).split(".")[-1]
            # [filename][mdl]
            # [filename][xlsx][xlsm]

            split_file_name = file_name.split(".")[0]
            uploaded_file_name = split_file_name + "_" + data_type[0] + "." + file_extension

            file = self.upload_file_alt(target_folder, uploaded_file_name, file_content)



            new_file_url = file.properties["ServerRelativeUrl"]
            print("File url: {0}".format(new_file_url))

            #for testing you dafty remove later
            #########################



            ##################
            #data_type = "Clean data"
            #software_version = "3.1"

            
            update_properties = self.edit_uploaded_properties(file, uploaded_file_name, new_file_url, self.unit_dict, data_type, software_version)

            print(update_properties)
        else:
            target_url = "/Shared Documents/{0}".format(os.path.basename(file_path))
            File.save_binary(self.context, target_url, file_content)


    def upload_file_alt(self, target_folder, name, content):
        '''method that actually uploads the file to the sharepoint
        puts it in the target folder, with the name and content, 
        content being the actual data in the file
        it returns the sharepoint info about the file so we can
        find it again'''

        context = target_folder.context
        info = FileCreationInformation()
        info.content = content
        info.url = name
        info.overwrite = True
        target_file = target_folder.files.add(info)
        context.execute_query()
        return target_file

    def edit_uploaded_properties(self, file, file_name, new_file_url, unit_info_dict, data_type, software_version):

        #possible_properties_list = file.listitem_allfields

        file_info = self.context.web.get_file_by_server_relative_url(new_file_url)


        

        #file_data = 
        self.context.load(file_info)
        self.context.execute_query()
        list_items = file_info.listitem_allfields
        self.context.load(list_items)
        self.context.execute_query()

        field_editor = list_items.parent_list.fields.get_by_internal_name_or_title("GP SN")

        self.context.load(field_editor)
        self.context.execute_query()


        if field_editor.properties['ReadOnlyField']:
            field_editor.set_property('ReadOnlyField', False)
            field_editor.update()
            self.context.execute_query()

        #list_items.set_property("GPFamily", "sammy")

        for item in unit_info_dict:


            
            #print(item)
            #print(unit_info_dict[item])

            sharepoint_name = item.replace("_","")
            new_property_value = unit_info_dict[item]
            
            list_items.set_property(sharepoint_name, new_property_value)
            list_items.update()
            self.context.execute_query()
        

        #print(list_items.properties['GPFamily'])
        
        #GP Family work removed and implemented in tc_trigger_class
        #GP_Family = make_turbine_family(unit_info_dict)

        #list_items.set_property("GPFamily", GP_Family)
        #list_items.update()
        #context.execute_query()

        list_items.set_property("DataType", data_type)
        list_items.update()
        self.context.execute_query()

        list_items.set_property("ToolVersion", software_version)
        list_items.update()
        self.context.execute_query()


        return True

