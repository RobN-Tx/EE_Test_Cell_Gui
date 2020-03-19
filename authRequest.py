import wx
from wx import *

class AuthPanel(wx.Panel):
    '''panel for requesting users authentication
    just a button panel, the info goes in dialog'''


    def __init__(self, parent):
    
        wx.Panel.__init__(self, parent)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
    
        applyBtn = wx.Button(self, label="Apply")
        applyBtn.Bind(wx.EVT_BUTTON, parent.onApply)
        btnSizer.Add(applyBtn, 0, wx.ALL, 5)
        cancelBtn = wx.Button(self, label="Cancel")
        cancelBtn.Bind(wx.EVT_BUTTON, parent.onCancel)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)

        self.SetSizer(btnSizer)

class AuthRequestDialog(wx.Dialog):
    '''
    request and recieve the authentication data
    '''
    def __init__(self):
        '''constructor'''

        wx.Dialog.__init__(self, None, title="Auth Request")

        size = (80, -1)
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)

        #create the sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)


        #create some widgets on the dialog

        lbl = wx.StaticText(self, label="Enter Sharepoint Authentication")
        lbl.SetFont(font)
        mainSizer.Add(lbl, 0, wx.CENTER)


        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD) 
        usernameLbl = wx.StaticText(self, label="Username:", size=size)
        usernameLbl.SetFont(font)
        self.usernameTxt = wx.TextCtrl(self, value="")
        mainSizer.Add(self.rowBuilder([usernameLbl, self.usernameTxt]), 
                      0, wx.EXPAND)

        passwordLbl = wx.StaticText(self, label="Password:", size=size)
        passwordLbl.SetFont(font)
        self.passwordTxt = wx.TextCtrl(self, value="", style=wx.TE_PASSWORD)
        mainSizer.Add(self.rowBuilder([passwordLbl, self.passwordTxt]), 
                      0, wx.EXPAND)

        button_panel=AuthPanel(self) 
        mainSizer.Add(button_panel, 0, wx.CENTER)
        self.SetSizer(mainSizer)

        #define the authentication dictionary
        self.authentication_dict = {'username':'','password':''}

    def onApply(self, event):
        
        self.authentication_dict['username'] = self.usernameTxt.GetValue()

        if len(self.authentication_dict['username'].split("@")) < 2:
            self.authentication_dict['username'] = self.authentication_dict['username'] + "@ethosenergygroup.com"

        self.authentication_dict['password'] = self.passwordTxt.GetValue()

        self.Destroy()
        print("apply")

    def onCancel(self):

        self.Destroy()

    #----------------------------------------------------------------------
    def rowBuilder(self, widgets):
        """"""
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl, txt = widgets
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(txt, 1, wx.EXPAND|wx.ALL, 5)
        return sizer


if __name__ == "__main__":
    app = wx.App(False)
    dlg = AuthRequestDialog()
    dlg.ShowModal()
    app.MainLoop()