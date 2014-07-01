__author__ = 'matt'

class ExitHouse():
    def __init__(self, *args, **kwargs):
        # do stuff
        # initialize state variables
        # initialize publish channel for exithouseinprogress?
        # subscribe to event change events
        self.dooropen_f = kwargs.get("motionin_flag")
        self.motionin_f = args
        self.motionout_f = False
        self.motionouttimer_f = False
        print "groovy"

    #def reseteventstate(self):
        # reset all sub-event states
        # reset motion_in flag
        # reset door_open flag
        # reset motion_out flag
        # reset exithouseinprogress flag
        # print "ExitHouse:resetEventState"

    #def createRule(self):
        # supports configuration of rules via config ... not sure how to do this yet
        #print "ExitHouse:createRule"

    def evaluateRule(self, *args, **kwargs):
        # is door open?
        print "ExitHouse:evaluateRule: exatracting kwargs"

        for key in kwargs:
            if key == "dooropen_flag":
                self.dooropen_f = kwargs["dooropen_flag"]
            elif key == "motionin_flag":
                self.motionin_f = kwargs["motionin_flag"]
            elif key == "motionout_flag":
                self.motionout_f = kwargs["motionout_flag"]
            elif key == "motionouttimer_flag":
                self.motionouttimer_f = kwargs["motionouttimer_flag"]

        #print "updated kwargs: "
        #print self.dooropen_f, self.motionin_f, self.motionout_f, self.motionouttimer_f

        # construct exit rule logic
        # seccussful exit event witout timer expiration
        if (self.dooropen_f == True) and \
                (self.motionin_f == True) and \
                (self.motionout_f == True) and \
                (self.motionouttimer_f == False):
            self.ruleoutcome = True
            print "ExitHouse:EXIT EVENT"
        else:
            self.ruleoutcome = False
            print "ExitHouse:STILL IN THE HOUSE"

        #self.ruleoutcome = False
        print "ExitHouse:evaluateRule:ruleoutcome= " + str(self.ruleoutcome)

        return self.ruleoutcome

        #dooropen_flag = dooropencheck(doorname, time)
            # y - has there been motion within past 30s?
            # n -

    def updateState(self):
        # subscribe to publisher for event changes
        # update local vars based what is received
        print "ExitHouse:updateState"