__author__ = 'matt'

"""
Widget from which money can be added or removed from account.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""

import wx
from pubsub import pub
from pubsub.py2and3 import print_


class ChangerWidget(wx.Frame):

  def __init__(self, parent=None):
    wx.Frame.__init__(self, parent, -1, "Control View")

    #create control buttons
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.opendoor = wx.Button(self, -1, "Open Door")
    self.closedoor = wx.Button(self, -1, "Close Door")
    self.motionintrue = wx.Button(self, -1, "In House Motion True")
    self.motioninfalse = wx.Button(self, -1, "In House Motion False")
    self.motionouttrue = wx.Button(self, -1, "Out of House Motion True")
    self.motionoutfalse = wx.Button(self, -1, "Out of House Motion False")
    self.timerexpiredtrue = wx.Button(self, -1, "Time Has Expiredr")
    self.timerexpiredfalse = wx.Button(self, -1, "Timer Has Not Expired")

    # stretch the button accross the window
    sizer.Add(self.opendoor, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.closedoor, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.motionintrue, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.motioninfalse, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.motionouttrue, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.motionoutfalse, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.timerexpiredtrue, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.timerexpiredfalse, 0, wx.EXPAND|wx.ALL)
    self.SetSizer(sizer)

    # bind the button to a function
    self.opendoor.Bind(wx.EVT_BUTTON, self.onDoorOpen)
    self.closedoor.Bind(wx.EVT_BUTTON, self.onCloseDoor)

    self.motionintrue.Bind(wx.EVT_BUTTON, self.onMotionInTrue)
    self.motioninfalse.Bind(wx.EVT_BUTTON, self.onMotionInFalse)
    self.motionouttrue.Bind(wx.EVT_BUTTON, self.onMotionOutTrue)
    self.motionoutfalse.Bind(wx.EVT_BUTTON, self.onMotionOutFalse)
    self.timerexpiredtrue.Bind(wx.EVT_BUTTON, self.onTimerExpireTrue)
    self.timerexpiredfalse.Bind(wx.EVT_BUTTON, self.onTimeExpireFalse)

  def onDoorOpen(self, evt):
      pub.sendMessage("event_occuring", state="DOOR_OPEN")

  def onCloseDoor(self, evt):
      pub.sendMessage("event_occuring", state="DOOR_CLOSED")

  def onMotionInTrue(self, evt):
      pub.sendMessage("event_occuring", state="MOTION_IN_TRUE")

  def onMotionInFalse(self, evt):
      pub.sendMessage("event_occuring", state="MOTION_IN_FALSE")

  def onMotionOutTrue(self, evt):
      pub.sendMessage("event_occuring", state="MOTION_OUT_TRUE")

  def onMotionOutFalse(self, evt):
      pub.sendMessage("event_occuring", state="MOTION_OUT_FALSE")

  def onTimerExpireTrue(self, evt):
      pub.sendMessage("event_occuring", state="TIMER_EXPIRE_TRUE")

  def onTimeExpireFalse(self, evt):
      pub.sendMessage("event_occuring", state="TIMER_EXPIRE_FALSE")
