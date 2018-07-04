from syslogging.syslogging import *

formatter = Formatter(fmt='{level_name} {abc}| {message}',style='{')
logger = Logger(formatter=formatter)

# email_dispatcher = EmailDispatcher('manhnddev11@gmail.com', 'Gmail_1112', ['nguyendinhmanh11k58@gmail.com'])
console_dispatcher = ConsoleDispatcher()

# logger.attach_dispatcher(LogLevel.ERROR, email_dispatcher)
logger.attach_dispatcher(LogLevel.ERROR, console_dispatcher)

logger.log(LogLevel.ERROR,"Error")