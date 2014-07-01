__author__ = 'matt'


import pubsub
import exithouse
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
from wx_statuswin import View
from wx_controlwin import ChangerWidget



class Model:

  def __init__(self):
    print "Main:Model:initializing local variables ... "
    self.inhousestate = True
    self.motionin_flag = True
    self.motionout_flag = True
    self.dooropen_flag = False
    self.motionouttimer_flag = False
    self.initdict = {"motionin_flag": self.motionin_flag,
                "motionout_flag": self.motionout_flag,
                "dooropen_flag": self.dooropen_flag,
                "motionouttimer_flag": self.motionouttimer_flag}

  def exitEvent(self):
    #now tell anyone who cares that the value has been changed
    pub.sendMessage("location_changed", inhousestate=self.inhousestate)

  def entryEvent(self):
    #now tell anyone who cares that the value has been changed
    pub.sendMessage("location_changed", inhousestate=self.inhousestate)


class Controller:

  def __init__(self):
    self.model = Model()

    #set up the first frame which displays the current Model value
    self.view1 = View()
    self.view1.setinhousestate(self.model.inhousestate)


    #set up the second frame which allows the user to modify the Model's value
    self.view2 = ChangerWidget()

    self.view1.Show()
    self.view2.Show()

    pub.subscribe(self.runRuleCoverage, 'event_occuring')

  def runRuleCoverage(self, state):
    if state == "DOOR_OPEN":
        self.model.dooropen_flag = True
    elif state == "DOOR_CLOSED":
        self.model.dooropen_flag = False
    elif state == "MOTION_IN_TRUE":
        self.model.motionin_flag = True
    elif state == "MOTION_IN_FALSE":
        self.model.motionin_flag = False
    elif state == "MOTION_OUT_TRUE":
        self.model.motionout_flag = True
    elif state == "MOTION_OUT_FALSE":
        self.model.motionout_flag = False
    elif state == "TIMER_EXPIRE_TRUE":
        self.model.motionouttimer_flag = True
    elif state == "TIMER_EXPIRE_FALSE":
        self.model.motionouttimer_flag = False


    if (self.model.dooropen_flag == True) and \
                (self.model.motionin_flag == True) and \
                (self.model.motionout_flag == True) and \
                (self.model.motionouttimer_flag == False):
        self.model.inhousestate = False
        print "ExitHouse:EXIT EVENT"
    else:
        self.model.inhousestate = True
        print "ExitHouse:STILL IN THE HOUSE"


    if self.model.inhousestate == False:
        self.model.exitEvent()
    else:
        self.model.entryEvent()

def main():
    # do stuff

    # creating manual state changes
    #a = exithouse.ExitHouse(initdict)
    #initdict["dooropen_flag"] = True
    #ruleoutcome = a.evaluateRule(**initdict)
    #print "Main: outcome of ExitHouse:EvaluateRule: " + str(ruleoutcome)

    # creating windows that help create automatic state changes
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__

    print_('---- Starting main event loop ----')
    app.MainLoop()
    print_('---- Exited main event loop ----')






if __name__ == "__main__":
    print "Main:In __name__ of main()"
    main()
