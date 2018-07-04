import asyncio
import smtplib
from email.mime.text import MIMEText

async def test():
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

# loop = asyncio.get_event_loop()
# loop.run_until_complete(test())
# loop.close()
test()

print("runrun")