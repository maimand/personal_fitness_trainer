import smtplib
import ssl
from email.message import EmailMessage

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "personal.fitness000@gmail.com"
password = 'evohymayavnxcuky'


def send_email(email: str, code: str):
    msg = EmailMessage()
    msg.set_content('You code to register is: {}.'.format(code))

    msg['Subject'] = 'Activation code'
    msg['From'] = 'personal.fitness000@gmail.com'
    msg['To'] = email
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()


def send_disable_email(email: str):
    msg = EmailMessage()
    msg.set_content('You account has been enabled. Contact your admin for more information')

    msg['Subject'] = 'Account disable'
    msg['From'] = 'personal.fitness000@gmail.com'
    msg['To'] = email

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()


def send_enable_email(email: str):
    msg = EmailMessage()
    msg.set_content('You account has been enabled. You now can login with email and password registered')

    msg['Subject'] = 'Account enabled'
    msg['From'] = 'personal.fitness000@gmail.com'
    msg['To'] = email

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
