__author__ = 'matt'

"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

import wx
from pubsub import pub


class View(wx.Frame):
  def __init__(self, parent=None):
    wx.Frame.__init__(self, parent, -1, "Main View")

    sizer = wx.BoxSizer(wx.VERTICAL)
    text = wx.StaticText(self, -1, "In House Status")
    ctrl = wx.TextCtrl(self, -1, "")

    textdoor = wx.StaticText(self, -1, "Door Open Status")
    ctrldoor = wx.TextCtrl(self, -1, "")
    textinmotion = wx.StaticText(self, -1, "In House Motion Detected")
    ctrlinmotion = wx.TextCtrl(self, -1, "")
    textoutmotion = wx.StaticText(self, -1, "Out of House Motion Detected")
    ctrloutmotion = wx.TextCtrl(self, -1, "")
    texttimer = wx.StaticText(self, -1, "Event Timer Expired")
    ctrltimer = wx.TextCtrl(self, -1, "")
    sizer.Add(text, 0, wx.EXPAND|wx.ALL)
    sizer.Add(ctrl, 0, wx.EXPAND|wx.ALL)
    sizer.Add(textdoor, 0, wx.EXPAND|wx.ALL)
    sizer.Add(ctrldoor, 0, wx.EXPAND|wx.ALL)
    sizer.Add(textinmotion, 0, wx.EXPAND|wx.ALL)
    sizer.Add(ctrlinmotion, 0, wx.EXPAND|wx.ALL)
    sizer.Add(textoutmotion, 0, wx.EXPAND|wx.ALL)
    sizer.Add(ctrloutmotion, 0, wx.EXPAND|wx.ALL)
    sizer.Add(texttimer, 0, wx.EXPAND|wx.ALL)
    sizer.Add(ctrltimer, 0, wx.EXPAND|wx.ALL)

    self.SetSizer(sizer)
    self.stateCtrl = ctrl
    self.doorCtrl = ctrldoor
    self.inmotionCtrl = ctrlinmotion
    self.outmotionCtrl = ctrloutmotion
    self.timerCtrl = ctrltimer

    ctrl.SetEditable(False)
    ctrldoor.SetEditable(False)
    ctrlinmotion.SetEditable(False)
    ctrloutmotion.SetEditable(False)
    ctrltimer.SetEditable(False)


    #subscribe to all "MONEY CHANGED" messages from the Model
    #to subscribe to ALL messages (topics), omit the second argument below
    pub.subscribe(self.setinhousestate, "location_changed")
    pub.subscribe(self.statechange, "event_occuring")

  def setinhousestate(self, inhousestate):
    print "View:setinhousestate:state= " +str(inhousestate)
    self.stateCtrl.SetValue(str(inhousestate))
    if inhousestate == True:
        self.stateCtrl.SetBackgroundColour("Green")
    else:
        self.stateCtrl.SetBackgroundColour("Red")


  def statechange(self, state):
    if state == "DOOR_OPEN":
            self.doorCtrl.SetValue("True")
    elif state == "DOOR_CLOSED":
            self.doorCtrl.SetValue("False")
    elif state == "MOTION_IN_TRUE":
            self.inmotionCtrl.SetValue("True")
    elif state == "MOTION_IN_FALSE":
            self.inmotionCtrl.SetValue("False")
    elif state == "MOTION_OUT_TRUE":
            self.outmotionCtrl.SetValue("True")
    elif state == "MOTION_OUT_FALSE":
            self.outmotionCtrl.SetValue("False")
    elif state == "TIMER_EXPIRE_TRUE":
            self.timerCtrl.SetValue("True")
    elif state == "TIMER_EXPIRE_FALSE":
            self.timerCtrl.SetValue("False")

