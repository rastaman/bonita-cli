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
        self.url = None
        if configuration is not None and 'url' in configuration:
            self.url = configuration['url']
        self.session = None
        self.platform_session = None

    def getConfiguration(self):
        return self.configuration

    def getInternalSession(self):
        if self.session is None:
            cookies = self.configuration['cookies']
            headers = { 
                'X-Bonita-API-Token': self.configuration['token']
            }
            self.session = requests.Session()
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
            self.session.headers = headers
        return self.session

    def getInternalPlatformSession(self):
        if self.platform_session is None:
            cookies = self.configuration['platform_cookies']
            headers = { 
                'X-Bonita-API-Token': self.configuration['platform_token']
            }
            self.platform_session = requests.Session()
            self.platform_session.cookies = requests.utils.cookiejar_from_dict(cookies)
            self.platform_session.headers = headers
        return self.platform_session

    def formatResponse(self, response):
        if response.text is not None and response.text != '':
            try:
                return [response.status_code, json.dumps(json.loads(response.text), indent=True)]
            except:
                return [response.status_code, response.text]
        return [response.status_code, None]
        
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
        r = self.getInternalSession().get( self.url + '/logoutservice')
        return r.status_code

    def getSession(self):
        r = self.getInternalSession().get( self.url + '/API/system/session/unusedid')
        return self.formatResponse(r)

    # System tenant API

    def getCurrentTenant(self):
        r = self.getInternalSession().get( self.url + '/API/system/tenant/unusedid')
        return self.formatResponse(r)

    def toggleTenantState(self, state):
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({'paused': state})
        r = self.getInternalSession().put( self.url + '/API/system/tenant/unusedid', headers=headers, data=payload)
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
        files = {'file': open(filename + extension, 'rb')}
        r = self.getInternalSession().post(self.url + '/portal/' + uploadType + 'Upload', files=files)
        return self.formatResponse(r)

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
        r = self.getInternalPlatformSession().get( self.url + '/platformlogoutservice?redirect=false')
        return r.status_code

    def getPlatform(self):
        r = self.getInternalPlatformSession().get( self.url + '/API/platform/platform/unusedid')
        return self.formatResponse(r)

    def togglePlatformState(self, state):
        payload = json.dumps({'state': state})
        headers = { 'Content-Type': 'application/json' }
        r = self.getInternalPlatformSession().put( self.url + '/API/platform/platform/unusedid', data=payload, headers=headers)
        return r.status_code

    # Process API

    def deployProcess(self, server_filename):
        payload = json.dumps({'fileupload': server_filename})
        headers = { 'Content-Type': 'application/json' }
        r = self.getInternalSession().post( self.url + '/API/bpm/process', data=payload, headers=headers)
        return self.formatResponse(r)
    
    def getProcess(self, process_id):
        r = self.getInternalSession().get( self.url + '/API/bpm/process/' + process_id)
        return self.formatResponse(r)

    def updateProcess(self, process_id, payload):
        headers = { 'Content-Type': 'application/json' }
        r = self.getInternalSession().put( self.url + '/API/bpm/process/' + process_id, data=payload, headers=headers)
        return self.formatResponse(r)

    def enableProcess(self, process_id):
        return self.updateProcess(process_id, json.dumps({'activationState': 'ENABLED'}))

    def disableProcess(self, process_id):
        return self.updateProcess(process_id, json.dumps({'activationState': 'DISABLED'}))

    # Portal API

    def deployPage(self, server_filename):
        payload = json.dumps({'pageZip': server_filename})
        headers = { 'Content-Type': 'application/json' }
        r = self.getInternalSession().post( self.url + '/API/portal/page ', data=payload, headers=headers)
        return self.formatResponse(r)

    def getPage(self, page_id):
        r = self.getInternalSession().get( self.url + '/API/portal/page/' + page_id)
        return self.formatResponse(r)

    def updatePage(self, page_id, server_filename):
        payload = json.dumps({'pageZip': server_filename})
        headers = { 'Content-Type': 'application/json' }
        r = self.getInternalSession().put( self.url + '/API/portal/page/' + page_id, data=payload, headers=headers)
        return self.formatResponse(r)
