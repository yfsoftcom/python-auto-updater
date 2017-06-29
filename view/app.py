#-*-<coding=UTF-8>-*-
import wx, os

class App(wx.App):

  def OnInit(self):
    return True

  def startup(self, view):
    self.view = view
    self.view.Show()
    self.MainLoop()