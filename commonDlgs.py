import wx
from wx import  *


#----------------------------------------------------------------------
def showMessageDlg(message, caption, flag=wx.ICON_ERROR):
    """"""
    msg = wx.MessageDialog(None, message=message,
                           caption=caption, style=flag)
    msg.ShowModal()
    msg.Destroy()


#def showList(list):
#    
#    text = wx.TextCtrl(panel,style = wx.TE_MULTILINE) 
#    lst = wx.ListBox(panel, size = (100,-1), choices = languages, style = wx.LB_SINGLE)


def textInputDlg(message, caption, valueString = ""):

    #frame = wx.Frame(None, -1, 'win.py')
    #frame.SetDimensions(0,0,200,50)
    text = wx.TextEntryDialog(None, message, caption, value = valueString)
    #text.SetValue("")
    if text.ShowModal() == wx.ID_OK:
        input_text = text.GetValue()
    text.Destroy()

    return input_text