from abc import ABC, abstractclassmethod
import sys, os, time, getpass
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from multiprocessing import Process, Queue

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
        try:
            return LogLevel._level2name[level]
        except Exception as e:
            sys.stderr.write('Erorr. Log level {} doesn\'t exits\n'.format(level))
            sys.stderr.write(str(e))            
            return None

    @staticmethod
    def get_level_by_name(name):
        try:
            return LogLevel._name2level[name.lower()]
        except Exception as e:
            sys.stderr.write('Error. There\'s no log level of level name {}'.format(name))
            sys.stderr.write(str(e))
            return None

class LogRecord: 
    def __init__(self, name='', level=LogLevel.INFO, msg=''):
        self.name = name
        self.level = level
        self.level_name = LogLevel.get_level_name(self.level)
        self.message = msg
        self.username = getpass.getuser()
        self.created_at = time.time()

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
    log_record_to_check_valid_fmt = LogRecord()

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
        if not self.valid_format():
            return None
        if self.use_time():
            record.created_at = self.format_datetime(record)
        if self.style == self._STYLES['PERCENT']:
            return self.fmt % record.__dict__
        elif self.style == self._STYLES['STRFORMAT']:
            return self.fmt.format(**record.__dict__)
        else:
            sys.stderr.write("Error. Format style {} doesn't exit\n".format(self.style))
            return None
    
    def valid_format(self):
        try:
            if self.style == self._STYLES['PERCENT']:
                self.fmt % self.log_record_to_check_valid_fmt.__dict__
            elif self.style == self._STYLES['STRFORMAT']:
                self.fmt.format(**self.log_record_to_check_valid_fmt.__dict__)
            return True
        except Exception as e: 
            return False
        
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
        except Exception as e:
            sys.stderr.write('Something wrong when deattach dispatcher!\n')
            sys.stderr.write(str(e))
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
        for level, dispatchers in self.registryDipatchers.items():
            if level == log_record.level:
                for dispatcher in dispatchers:
                    return dispatcher.log(log_msg)
        sys.stderr.write('Erorr. Log level or dispatcher don\'t work.')
        return 1
        
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
    def __init__(self, from_username, from_pass, to_mail_list=None):
        if not self.valid_to_mail_list_param:
            raise ValueError("Mail must be a string or a list")
        self.from_username = from_username
        self.from_pass = from_pass
        self.to_mail_list = to_mail_list
        self.get_to_mail_list()
        print(self.to_mail_list)

        mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(self.from_username, from_pass)
        self.mail_server = mail_server
        self.msg_queue = Queue()
        #process check queue & send mail
        p_send_mail = Process(target=self.send_mail)
        p_send_mail.start()

    def valid_to_mail_list_param(self):
        return self.to_mail_list != None and isinstance(self.to_mail_list, (str, list,))

    def get_to_mail_list(self):
        try: 
            if isinstance(self.to_mail_list, str):
                self.to_mail_list = self.to_mail_list.split(',')
                return 0
            elif isinstance(self.to_mail_list, list):
                self.to_mail_list = list
                return 0
            return None
        except Exception as e:
            sys.stderr.write('Error. Some erorrs has occured when extract to_mail_list')
            sys.stderr.write(str(e))
            return None

    def log(self, log_msg):
        if not self.valid_to_mail_list_param():
            sys.stderr.write('Error. Mail list not valid')            
            return 1
        self.msg_queue.put(log_msg)
        return 0
    
    def send_mail(self):
        try:
            while True:
                log_msg = self.msg_queue.get()
                msg = MIMEText(log_msg)
                msg['Subject'] = '[SYSLOGGING]'
                msg['From'] = self.from_username
                msg['to'] = self.from_username
                msg['cc'] = self.to_mail_list
                print(log_msg)
                self.mail_server.sendmail(self.from_username, self.to_mail_list, msg.as_string())
                self.mail_server.quit()
        except Exception as e:
            print(str(e))
            return None