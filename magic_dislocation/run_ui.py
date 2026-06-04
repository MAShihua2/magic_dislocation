
# https://blog.csdn.net/weixin_46065598/article/details/124332228
## Must to use the pythonw to run the wxPython GUI application
import wx
from magic_dislocation.ui import MainFrame

class MyPanel(wx.Panel):

    def __init__(self, parent):

        super().__init__(parent)
        button = wx.Button(self, label='Press Me')

class MagicDislocationAPP(wx.App):

    def OnInit(self):

        MainFrame().Show()
        return True

if __name__ == '__main__':
    
    app = MagicDislocationAPP()

    app.MainLoop()