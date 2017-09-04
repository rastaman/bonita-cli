import requests
import json
import os


class BonitaClient:

    UPLOAD_TYPES = {
        'file': [],
        'process': ['.bar'],
        'organization': ['.xml'],
        'actors': ['.xml'],
        'image': [ '.png', '.jpg', '.gif', '.jpeg', '.bmp', '.wbmp', '.tga'],
        'page': ['.zip'],
        'applications': ['.xml'],
        'connector' : ['.zip'],
        'report': [],
        'resource': ['.jar'],
        'profiles': ['.xml']
    }

    def __init__(self, configuration):
        self.configuration = configuration

    def getConfiguration(self):
        return self.configuration

    # Session API

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
        if r.text is not None and r.text != '':
            return [r.status_code, json.dumps(json.loads(r.text), indent=True)]        
        return [ r.status_code, None]

    # Tenant API

    def getCurrentTenant(self):
        url = self.configuration['url']
        cookies = self.configuration['cookies']
        r = requests.get( url + '/API/system/tenant/unusedid', cookies=cookies)
        if r.text is not None and r.text != '':
            return [r.status_code, json.dumps(json.loads(r.text), indent=True)]
        return [ r.status_code, None]

    def toggleTenantState(self, state):
        url = self.configuration['url']
        cookies = self.configuration['cookies']
        headers = {
            'X-Bonita-API-Token': self.configuration['token'],
            'Content-Type': 'application/json'
        }
        payload = json.dumps({'paused': state})
        r = requests.put( url + '/API/system/tenant/unusedid', cookies=cookies, headers=headers, data=payload)
        return r.status_code

    # Upload API

    def upload(self, uploadType, uploadFilename):
        if uploadType not in BonitaClient.UPLOAD_TYPES:
            return [-1, 'Unsupported upload type: %s' % uploadType]
        filename, extension = os.path.splitext(uploadFilename)
        exts = BonitaClient.UPLOAD_TYPES.get(uploadType)
        if len(exts) != 0 and not extension in exts:
            msg = 'Unsupported extension %s for upload type %s (supported: %s)' % (extension, uploadType, exts)
            return [ -2, msg]
        url = self.configuration['url']
        cookies = self.configuration['cookies']
        headers = { 'X-Bonita-API-Token': self.configuration['token'] }
        files = {'file': open(filename + extension, 'rb')}
        r = requests.post(url + '/portal/' + uploadType + 'Upload', files=files, headers=headers, cookies=cookies)
        return [r.status_code, r.text]
    
    # Platform api
    
    def platformLogin(self, url, username, password):
        payload = {
            'username': username,
            'password': password,
            'redirect': 'false'
        }

        r = requests.post( url + '/platformloginservice', data=payload, headers= {
                'Content-Type': 'application/x-www-form-urlencoded',
                'charset': 'utf-8'
        })

        if r.status_code == 200:
            cookies = requests.utils.dict_from_cookiejar(r.cookies)
            self.configuration['url'] = url
            self.configuration['platform_cookies'] = cookies
            self.configuration['platform_token'] = cookies['X-Bonita-API-Token']

        return r.status_code
    
    def platformLogout(self):
        url = self.configuration['url']
        cookies = self.configuration['platform_cookies']
        r = requests.get( url + '/platformlogoutservice?redirect=false', cookies=cookies)
        return r.status_code

    def getPlatform(self):
        url = self.configuration['url']
        cookies = self.configuration['platform_cookies']
        headers = { 'X-Bonita-API-Token': self.configuration['platform_token'] }
        r = requests.get( url + '/API/platform/platform/unusedid', cookies=cookies, headers=headers)
        if r.text is not None and r.text != '':
            return [r.status_code, json.dumps(json.loads(r.text), indent=True)]
        return [r.status_code, None]
    
    def togglePlatformState(self, state):
        url = self.configuration['url']
        cookies = self.configuration['platform_cookies']
        payload = json.dumps({'state': state})
        headers = { 'X-Bonita-API-Token': self.configuration['platform_token'], 'Content-Type': 'application/json' }
        r = requests.put( url + '/API/platform/platform/unusedid', cookies=cookies, data=payload, headers=headers)
        return r.status_code

