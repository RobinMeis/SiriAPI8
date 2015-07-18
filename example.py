#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SiriAPI8.SiriAPI import *

def hello(q, wildcards): #Answer function
    print ("You said Hello to " + wildcards[0])

SiriAPI = SiriAPI("icloud_mail@me.com", "Password") #Create SiriAPI8 object
print(SiriAPI.get_version())

SiriAPI.action.add([['hello', '*']], hello) #Add answer function for hello *

SiriAPI.connect() #Connect to iCloud

input("Press any key...\n")
SiriAPI.disconnect() #Close connection
