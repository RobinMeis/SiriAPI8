import imaplib
import time
import email
import sys

if (len(sys.argv) != 3):
    print("You didn't enter the correct parameters!\n   Example: python3 test.py email@me.com mypassword")
    exit()

username = sys.argv[1]
password = sys.argv[2]

keyword = '"iphone"' #TODO: idiotensicher machen! (anführungszeichen)

imap = imaplib.IMAP4_SSL("imap.mail.me.com", "993")
imap.login(username, password)
#print (imap.list()[1][0]) eventuell zum testen ob notes aktiviert sind, .status zum testen der verbindung

imap.select("Notes")
#print(imap.search(None, "ALL"))
#print(str(imap.fetch(imap.search(None, "ALL")[-1], "(RFC822)")[0][1]))


typ, data = imap.search(None, 'BODY', keyword) #Delete old commands with keyword (TODO: deal with option in future)
for num in data[0].split():
    #print("Deleted: " + str(num))
    imap.store(num, '+FLAGS', '\\Deleted')
imap.expunge()

stop = False

while (stop == False):
    if (imap.recent()[1][0] != None):
        time.sleep(1) #Sleeps prevent crashes (crazy and I don't know why)
        typ, data = imap.search(None, 'BODY', keyword) #Delete old commands with keyword (TODO: deal with option in future)
        for num in data[0].split():
            raw_email = imap.fetch(num, '(RFC822)')[1][0][1]
            email_message = email.message_from_bytes(raw_email)
            if email_message.is_multipart():
                for payload in email_message.get_payload():
                    # if payload.is_multipart(): ...
                    text = payload.get_payload()
            else:
                text = email_message.get_payload()

            text = text.replace("\n","").replace("\r","")
            if (text == "iPhone beenden"):
                stop = True
                print ("beenden")
            print (text)
            time.sleep(1)
            imap.store(num, '+FLAGS', '\\Deleted')
            imap.expunge()

        #data = imap.fetch(imap.search(None, 'BODY', '"reps"')[1][0].split()[-1], "(RFC822)") # fetch lates note

        #raw_email = data[1][0][1]
        #print (raw_email)
        #imap.store(latest_email_id, '+FLAGS', '\\Deleted')
        #imap.expunge()
    time.sleep(1)

imap.logout()
