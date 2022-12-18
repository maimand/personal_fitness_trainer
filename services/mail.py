import smtplib
import ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "personal.fitness000@gmail.com"
password = 'evohymayavnxcuky'


def send_email(email: str, code: str):
    message = """\
    Subject: Hi there

    You code to register is: {}.""".format(code)
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message)


def send_disable_email(email: str):
    message = """\
    Subject: Hi there

    You account has been disabled by admin. Please contact our website to reach for help."""
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message)


def send_enable_email(email: str):
    message = """\
    Subject: Hi there

    You account has been enabled. You now can login with email and password registered."""
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message)
