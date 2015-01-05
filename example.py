from SiriAPI8.SiriAPI import *

siriAPI = SiriAPI("my_email@me.com", "my_password")
siriAPI.connect()
input("Press any key...\n")
siriAPI.disconnect()
