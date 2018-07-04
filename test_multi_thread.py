from threading import Thread
import smtplib
from email.mime.text import MIMEText

def test():
    msg = MIMEText("Message here")
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = '[SYSLOGGING]'
    msg['From'] = 'nguyendinhmanh11k58@gmail.com'
    msg['To'] = 'nguyendinhmanh11k58@gmail.com'
    msg['From'] = 'nguyendinhmanh11k58@gmail.com'

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("manhnddev11@gmail.com", "Gmail_1112")
    server.sendmail('manhnddev11@gmail.com', ['nguyendinhmanh11k58@gmail.com'], msg.as_string())
    server.quit()
    return 0

def other_func():
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")
    print("1")

class main():
    thread_sendmail = Thread(target=test)
    thread_sendmail.start()
    print("printted to console!")
    other_func()

main()