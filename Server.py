import requests
import base64

#The __init__ method takes IPAddress, Username and Password as parameters
#The login method does the authentication part.If the authentication is correct
#it returns a session or else it returns a error message
class Server():
    def __init__(self, url, user, password, sslVerify=False):
       self.root_url = url
       self.user = user
       self.password = password
       self.sslVerify = sslVerify

    def login(self):
       session = requests.session()
       bstr = self.user + ':' + self.password
       #auth = base64.b64encode(bytes(bstr),'utf-8')
       bstr = bstr.encode('utf-8')
       auth = base64.b64encode(bstr)
       auth = auth.decode('utf-8')
       URL = self.root_url +'/api/space/user-management/login'
       headers = {'Authorization': 'Basic ' + auth}
       response = session.post(url=URL, headers= headers, verify=self.sslVerify)

       if response.status_code == 200:
         self.session = session
         return self

       else:
         raise Exception("Error: code = %d, text = %s" % (response.status_code, response.text))
