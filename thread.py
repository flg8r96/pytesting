# thread.py

from time import sleep
import mythread
import datetime

def hello(name):
    #sleep(2)
    print "Hello %s! The time is %s" % (name,datetime.datetime.now())
    

print "starting..."
print datetime.datetime.now()
rt = mythread.MyThread(1, hello, "World") # it auto-starts, no need of rt.start()
try:
    sleep(3) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!

