import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import os

from dotenv import load_dotenv
load_dotenv()

def send_mail(my_obj):
    my_obj['flag'] = True
    mail_content = '''Unsafe driving was detected. Check attachments for the evidence.'''
    #The mail addresses and password
    sender_address = 'guvenlisurusihlali@gmail.com'
    sender_pass = os.getenv('SENDER_PASS')
    receiver_address = 'bbbaykarmail@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Distracted Driver Detection System'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'sample.png'
    attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('content-disposition', 'attachment',
                    filename='%s' % 'sample.png')
    message.attach(payload)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    time.sleep(10)
    my_obj['flag'] = False



