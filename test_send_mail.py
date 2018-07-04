import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

_from = 'manhnddev11@gmail.com'
_to = ['nguyendinhmanh11k58@gmail.com', 'manhnddev11@gmail.com']

mail_server = smtplib.SMTP('smtp.gmail.com', 587)
mail_server.ehlo()
mail_server.starttls()
mail_server.ehlo()
mail_server.login(_from, 'Gmail_1112')
msg = MIMEText('Test')
msg['Subject'] = '[SYSLOGGING]'
msg['From'] = 'manhnddev11@gmail.com'
# msg['to'] = self.from_username
msg['cc'] = _to
mail_server.sendmail(_from, ','.join(_to), msg.as_string())
mail_server.quit()