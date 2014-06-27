"""
Adapted from wxPython website at http://wiki.wxpython.org/ModelViewController/.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""
# another small change

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
    pub.sendMessage("timer_changed", money=self.timerValue)


  def stopTimer(self, amount):
    self.timerValue = amount
    pub.sendMessage("timer_changed", money=self.timerValue)

  def changeTimer(self, amount):
    print "Model:changeTimer  amount: " + str(amount)
    self.timerValue = self.timerValue - amount
    #if self.timerValue > 0:
    #    pub.sendMessage("timer_counting", amount=1)
        #pub.sendMessage("timer_counting", amount=1) # timer value is not zero, set another interrupt for 1s duration
    pub.sendMessage("timer_changed", money=self.timerValue)

class Controller:

  def __init__(self):
    self.timerResetValue = 5
    self.model = Model()

    #set up the first frame which displays the current Model value
    self.view1 = View()
    self.view1.setTimerView(self.model.timerValue)

    #set up the second frame which allows the user to modify the Model's value
    self.view2 = ChangerWidget()
    self.view2.setTimerButtonText(self.timerResetValue)

    self.view1.Show()
    self.view2.Show()

    # Notify MODEL and persist data ...
    pub.subscribe(self.model.startTimer, 'timer_starting')  # when a timer is started
    pub.subscribe(self.model.stopTimer, 'timer_stopping')   # when a timer is stopped
    pub.subscribe(self.model.changeTimer, 'timer_changing') # when a timer changes it's value

  #  self.timerThread(amount=99)
    # Notify VIEW ...
  #  pub.subscribe(self.timerThread, 'timer_counting')   # when a timer changes it's value
    pub.subscribe(self.timerThread, 'timer_starting')   # when a timer starts

  def timerThread(self, amount):
      print "Controller: timerThread being initialized"
      rt = mythread.MyThread(self.timerResetValue, 1, self.model.changeTimer, 1) # it auto-starts, no need of rt.start()
      #rt = mythread.MyThread(5, 1, self.doNothing(), 1)

  def doNothing(self):
      print "Controller: I'm doing nothing"


if __name__ == "__main__":
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__

    print_('---- Starting main event loop ----')
    app.MainLoop()
    print_('---- Exited main event loop ----')
