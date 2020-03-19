import addModRecord
import authRequest
import commonDlgs
import controller
import os
import logging
import logging.config
import configparser
import getpass
import json
from threading import Thread
import time

from time import sleep

import wx
from wx import *
from ObjectListView import ObjectListView, ColumnDefn

import EE_Data.test_cell_interface_functions as tc
from EE_Data.tc_trigger_class import Gather_Class as Gatherer

#--extension-pkg-whitelist=pythoncom

import win32event
import pythoncom
import pywintypes
pythoncom.CoInitialize()

 

log_config_check = os.path.isfile('log_config.conf')
if log_config_check:
    # setup the config file based logger
    logging.config.fileConfig(fname='log_config.conf',
                              disable_existing_loggers=False)
    # Get the logger specified in the file
    logger = logging.getLogger("test_cell_logger")
else:
    input("Logging setup file not found. Hit enter to exit")

username = getpass.getuser()
print(username)

EVT_RESULT_ID = wx.NewId()
########################################################################

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)
 
class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data, parent_wx_object):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

        if self.data is True:
            parent_wx_object.Thread.run()
        elif self.data is False:
            parent_wx_object.startTestBtn.Enable()
            parent_wx_object.startBtn.Enable()

########################################################################
class WorkerThread(Thread):
    """Worker Thread Class."""
 
    #----------------------------------------------------------------------
    def __init__(self, wxObject, trigger):
        '''passs a fully instantiated trigger class'''
        """Init Worker Thread Class."""
        Thread.__init__(self)

        pythoncom.CoInitialize()
        self.trigger_instance = trigger
        self.wxObject = wxObject
        self.start()    # start the thread
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        #while True:
        pythoncom.CoInitialize()
        i=1
        for i in range(5):
            trigger_check = self.trigger_instance.trigger_read()

            if trigger_check:
                self.trigger_instance.run_performance_test()
            time.sleep(1)
            
        
        wx.PostEvent(self.wxObject, ResultEvent(self.wxObject.run_flag, self.wxObject))

    #----------------------------------------------------------------------



########################################################################
class ConfigPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):

        """Conostructor"""
        wx.Panel.__init__(self, parent)
        try:
            self.bookResults = controller.getAllRecords()
        except:
            self.bookResults = []



 
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        #searchSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        #font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD) 
 

        self.bookResultsOlv = ObjectListView(self, style=wx.LC_REPORT                
                                                        |wx.SUNKEN_BORDER)
        self.bookResultsOlv.SetEmptyListMsg("No Records Found")

        self.bookResultsOlv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onEditRecord)
        
        self.setBooks()
 
        # create the button row
        addRecordBtn = wx.Button(self, label="Add")
        addRecordBtn.Bind(wx.EVT_BUTTON, self.onAddRecord)
        btnSizer.Add(addRecordBtn, 0, wx.ALL, 5)
 
        editRecordBtn = wx.Button(self, label="Edit")
        editRecordBtn.Bind(wx.EVT_BUTTON, self.onEditRecord)
        btnSizer.Add(editRecordBtn, 0, wx.ALL, 5)
 
        deleteRecordBtn = wx.Button(self, label="Delete")
        deleteRecordBtn.Bind(wx.EVT_BUTTON, self.onDelete)
        btnSizer.Add(deleteRecordBtn, 0, wx.ALL, 5)
 
        showAllBtn = wx.Button(self, label="Show All")
        showAllBtn.Bind(wx.EVT_BUTTON, self.onShowAllRecord)
        btnSizer.Add(showAllBtn, 0, wx.ALL, 5)
 
        #mainSizer.Add(searchSizer)
        mainSizer.Add(self.bookResultsOlv, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(btnSizer, 0, wx.CENTER)
        self.SetSizer(mainSizer)

        self.Hide()
 
    #----------------------------------------------------------------------

    def onShowList(self, event):
        self.Hide()

    def onAddRecord(self, event):
        """
        Add a record to the database
        """
        
        dlg = addModRecord.AddModRecDialog()
        dlg.ShowModal()
        dlg.Destroy()
        self.showAllRecords()
 
    #----------------------------------------------------------------------
    def onEditRecord(self, event):
        """
        Edit a record
        """
        selectedRow = self.bookResultsOlv.GetSelectedObject()
        if selectedRow == None:
            commonDlgs.showMessageDlg("No row selected!", "Error")
            return
        dlg = addModRecord.AddModRecDialog(selectedRow, title="Modify",
                                           addRecord=False)
        dlg.ShowModal()
        dlg.Destroy()
        self.showAllRecords()
 
    #----------------------------------------------------------------------
    def onDelete(self, event):
        """
        Delete a record
        """
        selectedRow = self.bookResultsOlv.GetSelectedObject()
        if selectedRow == None:
            commonDlgs.showMessageDlg("No row selected!", "Error")
            return
        controller.deleteRecord(selectedRow.id)
        self.showAllRecords()
 
    #----------------------------------------------------------------------

    # 713528 0818
    def onSearch(self, event):
        """
        Searches database based on the user's filter choice and keyword
        """
        filterChoice = self.categories.GetValue()
        keyword = self.search.GetValue()
        print( "%s %s" % (filterChoice, keyword))
        self.bookResults = controller.searchRecords(filterChoice, keyword)
        self.setBooks()
 
    #----------------------------------------------------------------------
    def onShowAllRecord(self, event):
        """
        Updates the record list to show all of them
        """
        self.showAllRecords()
 
    #----------------------------------------------------------------------
    def setBooks(self):
        self.bookResultsOlv.SetColumns([
            ColumnDefn("Config Item", "left", 150, "title"),
            ColumnDefn("Commment", "left", 350, "comment"),
            ColumnDefn("Config Value", "left", 150, "config_value"),
            ColumnDefn("Is list?", "left", 100, checkStateGetter="is_list", checkStateSetter="is_list")
        ])

        self.bookResultsOlv.SetObjects(self.bookResults)
 
    #----------------------------------------------------------------------
    def showAllRecords(self):
        """
        Show all records in the object list view control
        """
        self.bookResults = controller.getAllRecords()
        self.setBooks()
 
########################################################################
class EEDataFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Ethos LT Test Cell",
                          size=(800, 600))

        self.logger = logging.getLogger('test_cell_logger.gui')
        
        self.run_flag = False
        self.authentication_dict = {'username':'','password':''}
        
        #panel = ConfigPanel(self)
        self.config_panel = ConfigPanel(self)
        self.start_panel = StartPanel(self)

        self.config_panel.Hide()

        #panel_sizer = wx.Pan
        self.btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
         # create the button row
        self.startBtn = wx.Button(self, label="Start")
        self.startBtn.Bind(wx.EVT_BUTTON, self.onStartEE_Data)
        self.btnSizer.Add(self.startBtn, 0, wx.ALL, 5)
 
        self.startTestBtn = wx.Button(self, label="Start Test Mode")
        self.startTestBtn.Bind(wx.EVT_BUTTON, self.onStartTesting)
        self.btnSizer.Add(self.startTestBtn, 0, wx.ALL, 5)

        self.stopBtn = wx.Button(self, label="Stop")
        self.stopBtn.Bind(wx.EVT_BUTTON, self.onStop)
        self.btnSizer.Add(self.stopBtn, 0, wx.ALL, 5)
 
        self.editConfigBtn = wx.Button(self, label="Edit Config")
        self.editConfigBtn.Bind(wx.EVT_BUTTON, self.onEditConfig)
        self.btnSizer.Add(self.editConfigBtn, 0, wx.ALL, 5)
 
        self.sizer.Add(self.btnSizer, 0, wx.CENTER)

        self.sizer.Add(self.config_panel, 1, wx.EXPAND)
        self.sizer.Add(self.start_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        logger.debug("started")

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()


        about_menu_item = fileMenu.Append(wx.ID_ANY, 
                                          "About", 
                                          "Some text")
        self.Bind(wx.EVT_MENU, self.onAboutClick, 
                  about_menu_item)
        menubar.Append(fileMenu, '&About')
        self.SetMenuBar(menubar)
        
        
        self.Show()

    def onStop(self, event):

        print("stop")

        self.run_flag = False

    def onStartEE_Data(self, event):

        self.run_flag = True
        print(self.run_flag)

        trigger_config = self.buildConfigDict()

        dlg = authRequest.AuthRequestDialog()

        dlg.ShowModal()

        trigger_config["authentication_dict"] = dlg.authentication_dict
    

        self.trigger = Gatherer(trigger_config, False)

        self.Thread = WorkerThread(self, self.trigger)

        self.startBtn.Disable()
        self.startTestBtn.Disable()

        print("start")

    def onStartTesting(self, event):

        self.run_flag = True
        print(self.run_flag)

        trigger_config = self.buildConfigDict()

        dlg = authRequest.AuthRequestDialog()

        dlg.ShowModal()

        trigger_config["authentication_dict"] = dlg.authentication_dict
    

        self.trigger = Gatherer(trigger_config, True)

        self.Thread = WorkerThread(self, self.trigger)

        self.startTestBtn.Disable()
        self.startBtn.Disable()

        print("start")

    def onAboutClick(self, event):
        """"""
        print("here we will set the about box info screen up")
        
        
    def onEditConfig(self, event):

        if self.config_panel.IsShown():
            self.SetTitle("Ethos Energy LT Performance Program")
            self.config_panel.Hide()
            self.start_panel.Show()
            self.editConfigBtn.SetLabel("Edit Config")

        else:
            self.SetTitle("Ethos Energy LT Performance Program - Configuration Page")
            self.config_panel.Show()
            self.start_panel.Hide()
            self.editConfigBtn.SetLabel("Finish Edit")
        self.Layout()

    def buildConfigDict(self):

        config_dict = {}
        for book in self.config_panel.bookResults:
            
            list_check = book.is_list

            if book.is_list:

                print(book.title, "is a list needs special treatment")

                #read in the dictionary
                value_dict = json.loads(book.config_value)

                #now see if it is processed as a dictionary or seperate lists

                if book.title.endswith("dict"):
                    config_dict[book.title] = value_dict
                
                elif book.title.endswith("tag"):
                    #split the dict into seperate lists one for key one for value
                    
                    
                    
                    config_dict[book.title + "_names"] = list(value_dict.keys())

                    config_dict[book.title + "_list"] = list(value_dict.values())

                else:
                    logger.error("config dictionary has list that doesnt end in dict or tag")

            else:
                config_dict[book.title] = book.config_value

        return config_dict



class StartPanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
         
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        #font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD) 
  
       

        mainSizer.Add(btnSizer, 0, wx.CENTER)
        self.SetSizer(mainSizer)


    def startEE_Data(self, event):


        dlg = authRequest.AuthRequestDialog()

        dlg.ShowModal()

        dlg.Destroy()

        print("start")

    def startTesting(self, event):

        print("test")

    def editConfig(self, event):

        self.Hide()

        return "return"


 
        
        #mainSizer.Add(searchSizer)

        


#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = EEDataFrame()
    app.MainLoop()