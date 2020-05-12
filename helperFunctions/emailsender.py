import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def sendMail(email,subject,messageTxt):
    s = smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()

    s.login("pamjje40@gmail.com","Cs322proj")
    msg = MIMEMultipart()

    msg['From']="pamjje40@gmail.com"
    msg['To']=email
    msg['Subject']=subject

    msg.attach(MIMEText(messageTxt,'plain'))

    s.send_message(msg)

    del msg

    s.quit()

#sendMail("pamjje40@gmail.com","This is a test","testing")
