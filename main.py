import wx.xrc
from main_window import BotFrame

if __name__ == "__main__":
    app = wx.App()
    frame = BotFrame(parent=None)
    frame.Show()
    app.MainLoop()