"""
Widget from which money can be added or removed from account.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""

# wx_win2.py

import wx
from pubsub import pub
from pubsub.py2and3 import print_


class ChangerWidget(wx.Frame):

  time = 30 # by how much money changes every time click

  def __init__(self, parent=None):
    wx.Frame.__init__(self, parent, -1, "Changer View")

    sizer = wx.BoxSizer(wx.VERTICAL)
    self.start = wx.Button(self, -1, "Start 30s Timer")
    self.stop = wx.Button(self, -1, "Stop 30s Timer")
    sizer.Add(self.start, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.stop, 0, wx.EXPAND|wx.ALL)
    self.SetSizer(sizer)

    self.start.Bind(wx.EVT_BUTTON, self.onStart)
    self.stop.Bind(wx.EVT_BUTTON, self.onStop)

  def onStart(self, evt):
      print_('----- Timer Starting PUB')
      pub.sendMessage("timer_starting", amount = self.time)

  def onStop(self, evt):
      print_('----- Timer Stoping PUB')
      pub.sendMessage("timer_stopping", amount = 0)
