from abc import ABC, abstractclassmethod
import sys, os, time, getpass
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

class LogLevel:
    INFO = 0
    DEBUG = 10
    WARNING = 20
    ERROR = 30
    FATAL = 40

    _level2name = {
        INFO: 'INFO',
        DEBUG: 'DEBUG',
        WARNING: 'WARNING',
        ERROR: 'ERROR',
        FATAL: 'FATAL'
    }

    _name2level = {
        'INFO': INFO,
        'DEBUG': DEBUG,
        'WARNING': WARNING,
        'ERROR': ERROR,
        'FATAL': FATAL
    }

    @staticmethod
    def valid_level(level):
        return level in LogLevel._level2name

    @staticmethod
    def get_level_name(level):
        return LogLevel._level2name[level]

class Formatter:
    _STYLES = {
        'PERCENT': '%',
        'STRFORMAT': '{'
    }
    _DEFAULT_FORMAT_PERCENT = '%(created_at)s %(level_name)s %(message)s'
    _DEFAULT_FORMAT_STRFORMAT = '{created_at} {level_name} {message}'
    _converter = time.localtime
    percent_time_search = '%(created_at)'
    strformat_time_search = '{created_at}'
    loggername_search = ['%(logger_name)', '{logger_name}']

    def __init__(self, fmt=None, datefmt='%Y-%m-%d %H:%M:%S', style=_STYLES['PERCENT']):
        self.datefmt = datefmt
        self.style = style
        if fmt is None:
            self.fmt = self._DEFAULT_FORMAT_PERCENT if style == Formatter._STYLES['PERCENT'] else self._DEFAULT_FORMAT_STRFORMAT
        else:
            self.fmt = fmt
            
    def use_time(self):
        return self.fmt.find(self.percent_time_search) >= 0 or self.fmt.find(self.strformat_time_search) >= 0

    def format_datetime(self, record):
        ct = self._converter(record.created_at)
        return time.strftime(self.datefmt, ct)

    def format(self, record):
        if self.use_time():
            record.created_at = self.format_datetime(record)

        if self.style == self._STYLES['PERCENT']:
            return self.fmt % record.__dict__
        elif self.style == self._STYLES['STRFORMAT']:
            return self.fmt.format(**record.__dict__)
        else:
            sys.stderr.write("Error. Format style {} doesn't exit".format(self.style))
            return None

class LogRecord: 
    def __init__(self, name='', level=LogLevel.INFO, msg=''):
        self.name = name
        self.level = level
        self.level_name = LogLevel.get_level_name(self.level)
        self.message = msg
        self.username = getpass.getuser()
        self.created_at = time.time()

class Logger:
    """
    Instances of the Logger class represent a single logging channel
    """
    def __init__(self, name='', formatter=None):
        self.name = name
        self.registryDipatchers = {}
        self.formatter = Formatter() if formatter is None else formatter

    def attach_dispatcher(self, level, dispatcher):
        if not LogLevel.valid_level(level):
            sys.stderr.write("Erorr. Log level {} doesn't exits\n".format(level))
            return 1
        if level not in self.registryDipatchers:
            self.registryDipatchers[level] = set([])
        self.registryDipatchers[level].add(dispatcher)
        return 0
        

    def deattach_dispatcher(self, level, dispatcher):
        if not LogLevel.valid_level(level):
            sys.stderr.write("Erorr. Log level {} doesn't exits\n".format(level))
            return 1
        try:
            if level in self.registryDipatchers and dispatcher in self.registryDipatchers[level]:
                self.registryDipatchers[level].remove(dispatcher)
            return 0
        except Exception:
            sys.stderr.write('Something wrong!\n')
            return 1       

    def log(self, level, msg):
        if not LogLevel.valid_level(level):
            sys.stderr.write("Erorr. Log level {} doesn't exits\n".format(level))
            return 1
        if msg is None:
            sys.stderr.write("Erorr. Log message can not be None\n")
            return 1
        log_record = LogRecord(level=level, msg=msg)
        log_msg = self.formatter.format(log_record)
        # print(self.formatter.format(log_record))
        for level, dispatchers in self.registryDipatchers.items():
            if level == log_record.level:
                for dispatcher in dispatchers:
                    dispatcher.log(log_msg)

class Dispatcher(ABC):
    @abstractclassmethod
    def log(self, log_msg):
        pass

class ConsoleDispatcher(Dispatcher): 
    def log(self, log_msg):
        try: 
            print(log_msg)
            return 0
        except Exception as e:
            sys.stderr.write('Failed to log to file: '+str(e))
            return 1

class FileDispatcher(Dispatcher):
    _DEFAULT_MODULE_FOLDER = '.syslogging'
    _DEFAULT_LOG_FOLDER = '{}/log'.format(_DEFAULT_MODULE_FOLDER)
    _DEFAULT_LOG_FILE = 'default.log'

    def __init__(self, pathname=None):
        if not os.path.exists(self._DEFAULT_MODULE_FOLDER):
            os.mkdir(self._DEFAULT_MODULE_FOLDER)
        if not os.path.exists(self._DEFAULT_LOG_FOLDER):
            os.mkdir(self._DEFAULT_LOG_FOLDER) 
        self.pathname = '{}/{}'.format(self._DEFAULT_LOG_FOLDER, self._DEFAULT_LOG_FILE) if pathname is None else pathname

    def log(self, log_msg):
        try:
            file = open(self.pathname, "a+")
            file.write('{}\n'.format(log_msg))
            return 0
        except Exception as e:
            sys.stderr.write('Failed to log to file: '+str(e))
            return 1

class EmailDispatcher(Dispatcher):
    def __init__(self, mail_list=None):
        if not self.valid_mail_list:
            raise ValueError("Mail must be a string or a list")
        self.mail_list = mail_list

    def valid_mail_list(self, mail_list):
        return True

    def log(self, log_msg):
        if self.mail_list is None:
            sys.stderr.write("WARNING. There's no mail list to log!")
            return 1
        msg = MIMEText(log_msg)

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = '[SYSLOGGING]'
        msg['From'] = 'nguyendinhmanh11k58@gmail.com'
        msg['To'] = 'nguyendinhmanh11k58@gmail.com'

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("manhnddev11@gmail.com", "")
        server.sendmail('manhnddev11@gmail.com', self.mail_list, msg.as_string())
        server.quit()