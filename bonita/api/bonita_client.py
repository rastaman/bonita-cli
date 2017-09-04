import requests
import token


class BonitaClient:

    def __init__(self, configuration):
        self.configuration = configuration

    def getConfiguration(self):
        return self.configuration
    
    def login(self, url, username, password):

        payload = {
            'username': username,
            'password': password,
            'redirect': 'false',
            'redirectURL': ''
        }

        r = requests.post( url + '/loginservice', data=payload, headers= {
                'Content-Type': 'application/x-www-form-urlencoded',
                'charset': 'utf-8'
        })

        if r.status_code == 200:
            cookies = requests.utils.dict_from_cookiejar(r.cookies)
            self.configuration['url'] = url
            self.configuration['cookies'] = cookies
            self.configuration['token'] = cookies['X-Bonita-API-Token']

        return r.status_code
    
    def logout(self):
        url = self.configuration['url']
        cookies = self.configuration['cookies']
        r = requests.get( url + '/logoutservice', cookies=cookies)
        return r.status_code

    def getSession(self):
        url = self.configuration['url']
        cookies = self.configuration['cookies']
        r = requests.get( url + '/API/system/session/unusedid', cookies=cookies)
        return [ r.status_code, r.text]
