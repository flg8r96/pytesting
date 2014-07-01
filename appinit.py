__author__ = 'matt'

class AppInit():
    def __init__(self, *args, **kwargs):
        #initialize stuff here
        global global_var
        global_var = 6


        print "appInit: initializing ..."
        print "appInit:self: " +str(self)
        print "appInit:args: " +str(args)
        print "appInit:kwargs: " +str(kwargs)
        print "appInit:globalvar: " +str(global_var)
        #appInit.initDB()

    def initdb(self):
        # make sure we can connect to the DB
        local_var = 77
        print "appInit:initDB: top of initDB"
        print "appInit:initDB:global_var " +str(global_var)
        return {"lv":local_var, "gv": [global_var, global_var, 1, 2, 3]}
        #return local_var, global_var

    def createGlobalVars(self):
        # create globals
        print "appInit: top of createGlobalVars"
