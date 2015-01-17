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
        self.version = "0.0.0" #TODO: Change version number on new release
        self.connection = None
        self.fetch = None
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

        try:
            self.connection = imaplib.IMAP4_SSL("imap.mail.me.com", "993") #Connect to server
        except:
            raise Exception("Connection to iCloud failed. Check your internet connection")

        try:
            self.connection.login(self.username, self.password) #Login
        except:
            raise Exception("Login to iCloud failed. Check user credentials")

        self.connection.select("Notes")

        #typ, data = self.connection.search(None, 'FROM', '"' + self.username + '"') #TODO: Dummy request, enable again if problems occour
        typ, data = self.connection.search(None, 'ALL', 'SUBJECT "' + self.keyword + '"') #Delete unhandled commands with keyword (TODO: deal with alternative execution in future)

        for num in data[0].split():
            self.connection.store(num, '+FLAGS', '\\Deleted')
        self.connection.expunge()
        self.fetch = threading.Thread(target=self.fetch)
        self.fetch.start()
        return (True)

    def get_version(self): #TODO: Reorder
        return (self.version)

    def disconnect(self):
        if (self.stop == False):
            self.stop = True
            self.fetch.join()
            #self.connection_check.join()

        if (self.connection != None):
            self.connection.logout()
            self.connection = None
        return (True)

    def __fetch(self):
        time.sleep(1)
        while (self.stop == False):
                recent = self.connection.recent() #Check for new notes
                if (recent[1][0] != None):
                    time.sleep(1) #Sleeps prevent crashes (crazy and I don't know why)
                    typ, data = self.connection.search(None, 'ALL', 'SUBJECT "' + self.keyword + '"') #Fetch new notes
                    for num in data[0].split():
                        raw_email = self.connection.fetch(num, '(RFC822)')[1][0][1]
                        email_message = email.message_from_bytes(raw_email)
                        if email_message.is_multipart(): #Parse content
                            for payload in email_message.get_payload():
                                text = payload.get_payload()
                        else:
                            text = email_message.get_payload()

                        text = text.replace("\n","").replace("\r","")
                        self.__search.search(text)
                        time.sleep(1)
                        self.connection.store(num, '+FLAGS', '\\Deleted')
                        self.connection.expunge()
                time.sleep(1)
        return()

    def __connection_check(self):
        while (self.stop == False):

            time.sleep(10)
