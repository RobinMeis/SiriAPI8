import imaplib
import email
import time
import threading

from .action import action
from .search import search

class SiriAPI:
    def __init__(self, username, password): #TODO: Implement error handling
        self.username = username
        self.password = password
        self.keyword = "iphone"
        self.version = "8.0.0" #TODO: Wiki explaination for versioning
        self.connection = None
        self.thread = None
        self.stop = True

        self.action = action()
        self.__search = search(self)

    def set_keyword(self, keyword="iphone"):
        if (isinstance(keyword, str)):
            self.keyword = keyword.lower()
        else:
            raise Exception("Keyword has to be a string")

    def version(self):
        return(version)

    def connect(self):
        self.stop = False
        self.connection = imaplib.IMAP4_SSL("imap.mail.me.com", "993") #Connect to server
        self.connection.login(self.username, self.password)
        self.connection.select("Notes")

        typ, data = self.connection.search(None, 'FROM', '"robin"')
        print(data)
        typ, data = self.connection.search(None, 'ALL', 'SUBJECT "' + self.keyword + '"') #Delete old commands with keyword (TODO: deal with option in future)
        print (data)
        for num in data[0].split():
            self.connection.store(num, '+FLAGS', '\\Deleted')
        self.connection.expunge()
        self.thread = threading.Thread(target=self.__thread)
        self.thread.start()
        return (True)


    def disconnect(self):
        self.stop = True
        self.thread.join()
        self.connection.logout()
        self.connection = None
        return (True)

    def __thread(self):
        time.sleep(1)
        while (self.stop == False):
            recent = self.connection.recent()
            if (recent[1][0] != None):
                print ("BP0")
                time.sleep(1) #Sleeps prevent crashes (crazy and I don't know why)
                typ, data = self.connection.search(None, 'ALL', 'SUBJECT "' + self.keyword + '"') #Delete old commands with keyword (TODO: deal with option in future)
                print ("BP1")
                print (typ)
                print (data)
                for num in data[0].split():
                    print ("BP2")
                    raw_email = self.connection.fetch(num, '(RFC822)')[1][0][1]
                    email_message = email.message_from_bytes(raw_email)
                    print ("BP3")
                    if email_message.is_multipart():
                        for payload in email_message.get_payload():
                            # if payload.is_multipart(): ...
                            text = payload.get_payload()
                    else:
                        text = email_message.get_payload()

                    text = text.replace("\n","").replace("\r","")
                    #print (text)
                    if (text == "iPhone beenden"):
                        print("beenden")
                    #print (text)
                    self.__search.search(text)
                    time.sleep(1)
                    self.connection.store(num, '+FLAGS', '\\Deleted')
                    self.connection.expunge()
            time.sleep(1)
