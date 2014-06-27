# mythread.py

from threading import Timer
import datetime


class MyThread(object):

#    def __init__(self, interval, function, *args, **kwargs):
    # interval = decrement step, duration = range
    def __init__(self, duration, interval, function, *args, **kwargs):
        self._timer     = None
        self.duration   = duration
        self.interval   = interval
#        print "MyThread:_init_ function is set to: " + str(function)
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.count 	    = self.duration
        print "MyThread: __init__" \
              + " time: " + str(datetime.datetime.now()) \
              + " function is set to: " + str(function) \
              + " duration: " +str(duration) \
              + " interval: " +str(interval)
        self.start()

    def _run(self):
        self.is_running = False
  #      print "MyThread:_run  args: " + str(self.args) + " kwargs: " + str(self.kwargs) +" function: " + str(self.function)
        print "MyThread:_run  args: " + str(self.count) \
              + " args: " + str(self.args) \
              + " kwargs: " + str(self.kwargs) \
              + " function: " + str(self.function) \
              + " count: " + str(self.count)
        self.count -= self.interval
        if self.count == 0:
            print "MyThread:_run if ... count=0 ... stopping."
            self.function(*self.args, **self.kwargs)
            self.stop()
        else:
            print "MyThread:_run else ... calling the function that was passed."
            self.start()
            self.function(*self.args, **self.kwargs)


  #      print "MyThread: _run " + str(self.count) + " time: " + str(datetime.datetime.now())

    def start(self):
        print "MyThread: start" + " time: " + str(datetime.datetime.now()) \
              + " interval: " + str(self.interval) \
              + " is_running: " + str(self.is_running)
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
  #          self._timer = Timer(self.duration, self._run)
            self._timer.start()
            self.is_running = True
   #         print "MyThread: start in if" + " time: " + str(datetime.datetime.now())

    def stop(self):
        print "MyThread: stop" + " time: " + str(datetime.datetime.now())
        self._timer.cancel()
        self.is_running = False
