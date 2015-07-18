#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib
import socket
import email
import time
import threading
import re

from .action import action
from .search import search

socket.setdefaulttimeout(2)

class SiriAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.keyword = "iphone"
        self.version = "8.0.2" #TODO: Change version number on new release
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

    def connect(self, start_thread=True):
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

        typ, data = self.connection.search(None, 'ALL', 'SUBJECT "' + self.keyword + '"') #Delete unhandled commands with keyword (TODO: deal with alternative execution in future)

        for num in data[0].split():
            self.connection.store(num, '+FLAGS', '\\Deleted')
        self.connection.expunge()

        if (start_thread == True):
            self.fetch = threading.Thread(target=self.__fetch)
            self.fetch.start()
        return (True)

    def disconnect(self):
        if (self.stop == False):
            self.stop = True
            self.fetch.join()

        if (self.connection != None):
            self.connection.logout()
            self.connection = None
        return (True)

    def __fetch(self):
        time.sleep(1)
        while (self.stop == False):
            try:
                recent = self.connection.recent() #Check for new notes
                if (recent[1][0] != None):
                    time.sleep(1)
                    typ, data = self.connection.search(None, 'ALL', 'SUBJECT "' + self.keyword + '"') #Fetch new notes
                    for num in data[0].split():
                        raw_email = self.connection.fetch(num, '(RFC822)')[1][0][1]
                        email_message = email.message_from_bytes(raw_email)
                        if email_message.is_multipart(): #Parse content
                            for payload in email_message.get_payload():
                                text = payload.get_payload()
                        else:
                            text = email_message.get_payload()
                        text = re.sub("<(.|\n)*?>", '', text)
                        self.connection.store(num, '+FLAGS', '\\Deleted')
                        self.connection.expunge()
                        text = text.replace("\n","").replace("\r","")
                        self.__search.search(text)
                        time.sleep(1)
                        adsad
                self.connection.noop()
                time.sleep(1)
            except socket.timeout: #Reconnect handler if connection is closed
                while (self.stop == False):
                    print("Connection failure")
                    try:
                        self.connection.logout()
                        print("Logout succesful")
                    except:
                        print("Couldn't logout")
                    self.connection = False
                    print("Trying to reconnect")
                    try:
                        self.connect(False)
                    except:
                        print("Reconnect failed")
                        time.sleep(5)
                    else:
                        print("Reconnected")
                        break
        return()

    def get_version(self):
        return (self.version)
