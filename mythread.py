# mythread.py

from threading import Timer
import datetime

class MyThread(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
	self.count 	= 0
	print "Thread: __init__" + " time: " + str(datetime.datetime.now())
        self.start()

    def _run(self):
        self.is_running = False
        #self.start()
        self.function(*self.args, **self.kwargs)
	self.count = self.count - 1
	print "Thread: _run " + str(self.count) + " time: " + str(datetime.datetime.now())
	# publish that the timer changed ... do so by covering it in the 'function'

    def start(self):
        print "Thread: start" + " time: " + str(datetime.datetime.now())
	if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
	    print "Thread: start in if" + " time: " + str(datetime.datetime.now())

    def stop(self):
	print "Thread: stop" + " time: " + str(datetime.datetime.now())
        self._timer.cancel()
        self.is_running = False
