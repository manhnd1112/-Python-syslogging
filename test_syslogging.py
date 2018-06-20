from syslogging import *


formatter = Formatter(fmt='{level_name} {message}', datefmt='%H:%M:%S', style='{')
logger = Logger('Test', formatter)
console_dispatcher = ConsoleDispatcher()

# attach & deattach dispatcher
logger.attach_dispatcher(LogLevel.INFO, console_dispatcher)
#print(logger.registryDipatchers)
logger.log(LogLevel.INFO, 'info log')

