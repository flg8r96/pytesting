"""
Adapted from wxPython website at http://wiki.wxpython.org/ModelViewController/.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""
# small change

import wx

from pubsub import pub
from pubsub.py2and3 import print_

print_('pubsub API version', pub.VERSION_API)

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys
useNotifyByWriteFile(sys.stdout)

# the following two modules don't know about each other yet will
# exchange data via pubsub:
from wx_win1 import View
from wx_win2 import ChangerWidget
import mythread

class Model:

  def __init__(self):
    self.timerValue = 0


  def startTimer(self, amount):
    self.timerValue = amount
    #now tell anyone who cares that the value has been changed
    pub.sendMessage("timer_changed", money=self.timerValue)
    self.controller = Controller()
    self.controller.changeTimerView(self.timerValue)


  def stopTimer(self, value):
    self.timerValue = value
    #now tell anyone who cares that the value has been changed
    pub.sendMessage("timer_changed", money=self.timerValue)

  def changeTimer(self, value):
    self.timerValue -= value
    pub.sendMessage("timer_changed", money=self.timerValue)

class Controller:

  def __init__(self):
    self.model = Model()

    #set up the first frame which displays the current Model value
    self.view1 = View()
    self.view1.setTimerView(self.model.timerValue)

    #set up the second frame which allows the user to modify the Model's value
    self.view2 = ChangerWidget()

    self.view1.Show()
    self.view2.Show()

    pub.subscribe(self.model.startTimer, 'timer_starting')
    pub.subscribe(self.model.stopTimer, 'timer_stopping')
    pub.subscribe(self.model.changeTimer, 'timer_changing')

  def changeTimerView(self, amount):
     # call timer tread
     rt = mythread.MyThread(1, self.model.changeTimer(amount), 1) # it auto-starts, no need of rt.start()
     
#    if amount >= 0:
#        self.model.startTimer(amount)
#    else:
#        self.model.stopTimer(-amount)


if __name__ == "__main__":
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__

    print_('---- Starting main event loop ----')
    app.MainLoop()
    print_('---- Exited main event loop ----')
