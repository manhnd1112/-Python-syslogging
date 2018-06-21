from syslogging.syslogging import *


formatter = Formatter(fmt='{created_at} {level_name} {message}', datefmt='%H:%M:%S', style='{')
logger = Logger('Test', formatter)
console_dispatcher = ConsoleDispatcher()
file_dispatcher = FileDispatcher()
email_dispatcher = EmailDispatcher(['nguyendinhmanh11k58@gmail.com'])
# attach & deattach dispatcher
logger.attach_dispatcher(LogLevel.INFO, console_dispatcher)
logger.attach_dispatcher(LogLevel.ERROR, console_dispatcher)
logger.attach_dispatcher(LogLevel.ERROR, file_dispatcher)
logger.attach_dispatcher(LogLevel.ERROR, email_dispatcher)
#print(logger.registryDipatchers)
logger.log(LogLevel.INFO, 'info log')
logger.log(LogLevel.ERROR, 'error')
