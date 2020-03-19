''' a learning script based on:
http://zetcode.com/wxpython/firststeps/
working out how to build a gui for EE test data'''

import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
            size=(800, 450))

        self.Centre()

        self.InitUI()

    def InitUI(self):

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()

        
        toyItem = fileMenu.Append(wx.ID_FILE1,"new", "New window")
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')


        menubar.Append(fileMenu, '&File')

        configMenu = wx.Menu()
        menubar.Append(configMenu,"Config")


        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)

        
        self.Bind(wx.EVT_MENU, self.OnToy, toyItem)

        self.SetSize((800, 450))
        self.SetTitle('Simple menu')
        self.Centre()

    def OnQuit(self, e):
        self.Close()
        
    def OnToy(self, e):
        new_frame = wx.Frame(None, title='Simple application')
        new_frame.Show()


def main():

    app = wx.App()
    ex = Example(None, title='Sizing')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()