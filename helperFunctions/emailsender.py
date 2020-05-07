import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

message_template = ""

s = smtplib.SMTP("smtp.gmail.com",587)
s.starttls()

s.login("","")

def sendMail(email,subject,messageTxt):
    msg = MIMEMultipart()

    message = messageTxt

    msg['From']="foo@gmail.com"
    msg['To']=email
    msg['Subject']=subject

    msg.attach(MIMEText(message,'plain'))

    s.send_message(msg)

    del msg

    s.quit()
sendMail("", "")
