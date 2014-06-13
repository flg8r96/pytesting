"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""
# wx_win1.py

import wx
from pubsub import pub


class View(wx.Frame):
  def __init__(self, parent=None):
    wx.Frame.__init__(self, parent, -1, "Main View")

    sizer = wx.BoxSizer(wx.VERTICAL)
    text = wx.StaticText(self, -1, "Timer")
    ctrl = wx.TextCtrl(self, -1, "")
    sizer.Add(text, 0, wx.EXPAND|wx.ALL)
    sizer.Add(ctrl, 0, wx.EXPAND|wx.ALL)

    self.moneyCtrl = ctrl
    ctrl.SetEditable(False)
    self.SetSizer(sizer)

    #subscribe to all "MONEY CHANGED" messages from the Model
    #to subscribe to ALL messages (topics), omit the second argument below
    pub.subscribe(self.setTimerView, "timer_changed")

  def setTimerView(self, money):
    self.moneyCtrl.SetValue(str(money))


