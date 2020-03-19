import time
import wx
 
from threading import Thread
 
# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

global stop_threads 

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)
 
class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data, parent_wx_onject):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

        if self.data is True:
            parent_wx_onject.Thread.run()
        elif self.data is False:
            parent_wx_onject.btn.Enable()


        

 
########################################################################
class TestThread(Thread):
    """Test Worker Thread Class."""
 
    #----------------------------------------------------------------------
    def __init__(self, wxObject):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.wxObject = wxObject
        self.start()    # start the thread
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        #while True:
        i=1
        for i in range(5):
            time.sleep(1)
            print(i)
            amtOfTime = (i + 1) * 1
            wx.PostEvent(self.wxObject, ResultEvent(amtOfTime, self.wxObject))
            
            
            
            #if stop_threads: 
                #break
        
        wx.PostEvent(self.wxObject, ResultEvent(self.wxObject.run_flag, self.wxObject))

    #----------------------------------------------------------------------

    def stop(self):
        self.stop()
 
########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial")
 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.displayLbl = wx.StaticText(panel, label="Amount of time since thread started goes here")
        self.btn = wx.Button(panel, label="Start Thread")

        self.btn2 = wx.Button(panel, label="Stop Thread")
 
        self.btn.Bind(wx.EVT_BUTTON, self.onButton)

        self.btn2.Bind(wx.EVT_BUTTON, self.offButton)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.displayLbl, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.btn, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.btn2, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)
 
        # Set up event handler for any worker thread results
        EVT_RESULT(self, self.updateDisplay)
 
    #----------------------------------------------------------------------
    def onButton(self, event):
        """
        Runs the thread
        """
        self.run_flag = True
        self.Thread = TestThread(self)
        #self.Thread.run(self)
        self.displayLbl.SetLabel("Thread started!")
        
        self.btn = event.GetEventObject()
        self.btn.Disable()
 
    #----------------------------------------------------------------------


    def offButton(self, event):

        self.run_flag = False
        self.displayLbl.SetLabel("Thread stopped?!")

    #----------------------------------------------------------------------

    def return_looper(self):

        print("hi")

        return "bye"


    #----------------------------------------------------------------------
    def updateDisplay(self, msg):
        """
        Receives data from thread and updates the display
        """
        t = msg.data
        if isinstance(t, int):
            self.displayLbl.SetLabel("Time since thread started: %s seconds" % t)
        else:
            self.displayLbl.SetLabel("%s" % t)
            self.btn.Enable()
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()