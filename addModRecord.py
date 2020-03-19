# addModRecord.py
# --extension-pkg-whitelist=wx

import commonDlgs
import controller
#import addListRecord
import json
import wx
from wx import * #Panel, BoxSizer, Button, ALL, EXPAND, Font

#from wx import *


class ButtonPanel(wx.Panel):
    """ Just a button panel """

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        okBtn = wx.Button(self, label="Save")
        okBtn.Bind(wx.EVT_BUTTON, parent.onRecord)
        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        cancelBtn = wx.Button(self, label="Close")
        cancelBtn.Bind(wx.EVT_BUTTON, parent.onClose)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)

        self.SetSizer(btnSizer)


class ListButtonPanel(wx.Panel):
    ''' button panel for adding to list'''

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)

        listBtnSizer = wx.BoxSizer(wx.HORIZONTAL)

        addListBtn = wx.Button(self, label="Add Below")
        addListBtn.Bind(wx.EVT_BUTTON, parent.onListAdd)
        listBtnSizer.Add(addListBtn, 0, wx.ALL, 5)

        delListBtn = wx.Button(self, label="Delete Selected")
        delListBtn.Bind(wx.EVT_BUTTON, parent.onListDelete)
        listBtnSizer.Add(delListBtn, 0, wx.ALL, 5)

        editListBtn = wx.Button(self, label="Edit Selected")
        editListBtn.Bind(wx.EVT_BUTTON, parent.onListEdit)
        listBtnSizer.Add(editListBtn, 0, wx.ALL, 5)

        self.SetSizer(listBtnSizer)

########################################################################


class AddModRecDialog(wx.Dialog):
    """
    Add / Modify Record dialog
    """

    # ----------------------------------------------------------------------
    def __init__(self, row=None, title="Add", addRecord=True):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="%s Records" % title)

        self.addRecord = addRecord
        self.selectedRow = row
        if row:
            bTitle = self.selectedRow.title

            config_value = self.selectedRow.config_value
            self.config_values_row = config_value
            comment = self.selectedRow.comment
            is_list = self.selectedRow.is_list
        else:
            bTitle = config_value = comment = is_list = ""
            self.config_values_row = ""
        size = (80, -1)
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)

        self.config_value_list = ""

        # create the sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # create some widgets
        lbl = wx.StaticText(self, label="Config Updater")
        lbl.SetFont(font)
        mainSizer.Add(lbl, 0, wx.CENTER)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)

        # make title widget row
        titleLbl = wx.StaticText(self, label="Title:", size=size)
        titleLbl.SetFont(font)
        self.titleTxt = wx.TextCtrl(self, value=bTitle)
        mainSizer.Add(self.rowBuilder([titleLbl, self.titleTxt]),
                      0, wx.EXPAND)

        # make is list check box row
        is_list_value_Lbl = wx.StaticText(
            self, label="Value is List:", size=size)
        is_list_value_Lbl.SetFont(font)
        self.is_list_chkBox = wx.CheckBox(self)

        self.is_list_chkBox.Value = bool(is_list)
        self.is_list_chkBox.Bind(wx.EVT_CHECKBOX, self.onListChkBox)
        mainSizer.Add(self.rowBuilder([is_list_value_Lbl, self.is_list_chkBox]),
                      0, wx.EXPAND)

        # setup config list value rows


        self.config_listLbl = wx.StaticText(
            self, label="Config Values:", size=size)
        self.config_listLbl.SetFont(font)
        self.config_listTxt = wx.ListCtrl(self,style=wx.LC_REPORT)
        
        self.config_listTxt.InsertColumn(1,'Tag Name', format=wx.LIST_FORMAT_CENTRE)

        self.config_listTxt.InsertColumn(2,'PLC Tag',format=wx.LIST_FORMAT_CENTRE)

        
        self.config_listTxt.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onListEdit)
        
        if is_list:
            self.fillTable()

        mainSizer.Add(self.rowBuilder([self.config_listLbl, self.config_listTxt]),
                      0, wx.EXPAND)

        self.list_button_panel = ListButtonPanel(self)
        mainSizer.Add(self.list_button_panel, 0, wx.CENTER)

        # now setup the single config value input
        self.config_valueLbl = wx.StaticText(
            self, label="Config Value:", size=size)
        self.config_valueLbl.SetFont(font)
        self.config_valueTxt = wx.TextCtrl(self, value=config_value)

        mainSizer.Add(self.rowBuilder([self.config_valueLbl, self.config_valueTxt]),
                      0, wx.EXPAND)

        # now call the method to update what is and isnt shown
        self.onListChkBox(None)

        # setup the comment row
        commentLbl = wx.StaticText(self, label="Comment:", size=size)
        commentLbl.SetFont(font)
        self.commentTxt = wx.TextCtrl(self, value=comment)
        mainSizer.Add(self.rowBuilder([commentLbl, self.commentTxt]),
                      0, wx.EXPAND)

        #now add the row panel and do the sizing of the window
        button_panel = ButtonPanel(self)
        mainSizer.Add(button_panel, 0, wx.CENTER)
        self.SetSizer(mainSizer)
        self.SetSize(425, self.BestSize.height)

    def fillTable(self, load_json = True):
        
        #clear out the table
        self.config_listTxt.DeleteAllItems()


        if self.config_values_row or self.config_value_list is not "":

            print("wasnt empty")

            if load_json:
                self.config_value_list = json.loads(self.config_values_row)

            for key in self.config_value_list:

                pair = (key, self.config_value_list[key])

                self.config_listTxt.Append(pair)

                self.Refresh()

                #print(item)
        
        else:

            print("was empty")

        if self.config_listTxt.GetItemCount():
             itemFrom = self.config_listTxt.GetTopItem()
             itemTo   = self.config_listTxt.GetTopItem()+1 + self.config_listTxt.GetCountPerPage()
             itemTo   = min(itemTo, self.config_listTxt.GetItemCount()-1)
             self.config_listTxt.RefreshItems(itemFrom, itemTo) 

    def onListChkBox(self, event):
        ''' method to select which of the input options is show
        checks if the 'is list' check box is true and then selects what to show
        '''

        if self.is_list_chkBox.GetValue():
            self.config_listLbl.Show()
            self.config_listTxt.Show()
            self.list_button_panel.Show()
            self.config_valueLbl.Hide()
            self.config_valueTxt.Hide()

        else:
            self.config_listLbl.Hide()
            self.config_listTxt.Hide()
            self.list_button_panel.Hide()
            self.config_valueLbl.Show()
            self.config_valueTxt.Show()

        #update window size
        self.SetSize(425, self.BestSize.height)

    # ----------------------------------------------------------------------
    def getListDict(self):

        # logic to serialise the list
        config_dict = {}
        i = 0

        while i < self.config_listTxt.ItemCount:
        
            config_dict[self.config_listTxt.GetItem(i,0).Text] = self.config_listTxt.GetItem(i, 1).Text
            i = i+1

        return config_dict
    # ----------------------------------------------------------------------

    def getData(self):
        """"""

        bookDict = {}

        #moved down to direct input
        #title = self.titleTxt.GetValue()

        #comment = self.commentTxt.GetValue()
        
        is_list = self.is_list_chkBox.GetValue()

        if is_list:
            
            config_value = json.dumps(self.getListDict(), ensure_ascii=True)


        else:
            config_value = self.config_valueTxt.GetValue()

        if self.titleTxt.GetValue() == "":
            commonDlgs.showMessageDlg("Title is Required!",
                                      "Error")
            return

        #if "-" in config_value:
            #config_value = config_value.replace("-", "")
        bookDict["title"] = self.titleTxt.GetValue()
        bookDict["config_value"] = config_value
        bookDict["comment"] = self.commentTxt.GetValue()
        bookDict["is_list"] = is_list

        return bookDict

    # ----------------------------------------------------------------------

    def onAdd(self):
        """
        Add the record to the database
        """
        bookDict = self.getData()
        data = ({"book": bookDict})
        controller.addRecord(data)

        # show dialog upon completion
        commonDlgs.showMessageDlg("Config value added",
                                  "Success!", wx.ICON_INFORMATION)

        # clear dialog so we can add another book
        for child in self.GetChildren():
            if isinstance(child, wx.TextCtrl):
                child.SetValue("")

    # ----------------------------------------------------------------------

    def onListAdd(self, event):

        new_item = commonDlgs.textInputDlg("Enter new item name", "New item")

        new_value = commonDlgs.textInputDlg("Enter new item value", "New value")

        i = 0

        output_dict = {}

        #case for if it is an empty list
        if self.config_listTxt.ItemCount is 0:
            output_dict[new_item] = new_value
        
        else:
            while i < self.config_listTxt.ItemCount:
            
                output_dict[self.config_listTxt.GetItem(i,0).Text] = self.config_listTxt.GetItem(i, 1).Text
                
                #insert new item in list below current selected item
                if i is self.config_listTxt.FocusedItem and self.config_listTxt.SelectedItemCount is 1:
                    output_dict[new_item] = new_value
                
                i = i+1

            #if no item in the list was selected we will add to the bottom
            if self.config_listTxt.SelectedItemCount is 0:
                output_dict[new_item] = new_value

        self.config_value_list = output_dict

        self.fillTable(False)

        self.SetSize(425, self.BestSize.height)


    # ----------------------------------------------------------------------

    def onListDelete(self, event):

        self.SetSize(425, self.BestSize.height)

        output_dict = {}

        if self.config_listTxt.SelectedItemCount is 1:

            i = 0

            while i < self.config_listTxt.ItemCount:

                if i is not self.config_listTxt.FocusedItem:

                    output_dict[self.config_listTxt.GetItem(i,0).Text] = self.config_listTxt.GetItem(i, 1).Text

                i = i + 1

            self.config_value_list = output_dict

            self.fillTable(False)
        

        #print(self.config_listTxt.FocusedItem)

        print("onlistDelete")
    # ----------------------------------------------------------------------



    def onListEdit(self, event):

        if self.config_listTxt.SelectedItemCount is 1:
        
            edit_key = self.config_listTxt.GetItem(self.config_listTxt.FocusedItem,0).Text

            edit_value = self.config_listTxt.GetItem(self.config_listTxt.FocusedItem,1).Text

            edit_value = commonDlgs.textInputDlg("Edit item", "Edit item", edit_value)
            
            self.config_value_list[edit_key] = edit_value

            self.fillTable(False)

            self.SetSize(425, self.BestSize.height)

    # ----------------------------------------------------------------------

    def onClose(self, event):
        """
        Cancel the dialog
        """
        self.Destroy()

    # ----------------------------------------------------------------------
    def onEdit(self):
        """"""
        bookDict = self.getData()
        #comboDict = dict(authorDict.items() + bookDict.items())
        controller.editRecord(self.selectedRow.id, bookDict)
        commonDlgs.showMessageDlg("Config Item Edited Successfully!", "Success",
                                  wx.ICON_INFORMATION)
        self.Destroy()

    # ----------------------------------------------------------------------
    def onRecord(self, event):
        """"""
        if self.addRecord:
            self.onAdd()
        else:
            self.onEdit()
        self.titleTxt.SetFocus()

    # ----------------------------------------------------------------------
    def rowBuilder(self, widgets):
        """"""
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl, txt = widgets
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(txt, 1, wx.EXPAND | wx.ALL, 5)
        return sizer


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    dlg = AddModRecDialog()
    dlg.ShowModal()
    app.MainLoop()
