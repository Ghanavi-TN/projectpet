import smtplib
import email
import imaplib
import os
from imap_tools import MailBox, Q
import random
import MySQLdb

def process(remail,subject,bom):
        sender_email="examevalutationmsclg@gmail.com"
        password="jdfxxynayjjjomjd"
        
        header = 'To:' + remail + '\n' + 'From: ' + sender_email + '\n' + 'Subject: ' + subject + '\n'
        msg = header + bom
        
        print("header",header)
        print("msg",msg)
                
        mail = smtplib.SMTP('smtp.gmail.com',587)    #host and port area
        mail.ehlo()  #Hostname to send for this command defaults to the FQDN of the local host.
        mail.starttls() #security connection
        mail.login(sender_email,password) #login part
        mail.sendmail(sender_email,remail,msg) #send part
        print ("Congrates! Your mail has send. ")
        mail.close()   
