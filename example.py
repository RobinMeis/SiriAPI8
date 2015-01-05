from SiriAPI8.SiriAPI import *

def hello (q, wildcards): #Here could react you script
    print ("Q: " + q)
    print (wildcards)

siriAPI = SiriAPI("my_icloud_mail@me.com", "my_password")

siriAPI.action.add([['hello', '*']], hello)
siriAPI.connect()

print (siriAPI.action.list())
input("Press any key...\n")
siriAPI.disconnect()
