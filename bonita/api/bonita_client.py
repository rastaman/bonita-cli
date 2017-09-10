import requests
import json
import os
import javaobj

#try:
#import logging
#import time
#    import http.client as http_client
#except ImportError:
#    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1
#logging.basicConfig(level=logging.DEBUG)
#logging.debug('--- %s ---', time.strftime("%H:%M:%S"))


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

    CLASSNAME_STRING_PARAMETER = """<object-stream>
  <list>
    <string>java.lang.String</string>
  </list>
</object-stream>"""

    CLASSNAME_VOID_PARAMETER = """<object-stream>
  <list/>
</object-stream>"""

    CLASSNAME_BINARY_PARAMETER = """<object-stream>
  <list>
    <string>[B</string>
  </list>
</object-stream>"""

    VALUE_STRING_PARAMETER = """<object-stream>
  <object-array>
    <string>{}</string>
  </object-array>
</object-stream>"""

    VALUE_NULL_PARAMETER = """<object-stream>
  <null/>
</object-stream>"""

    VALUE_BINARY_PARAMETER = """<object-stream>
  <object-array>
    <string>==ByteArray==</string>
  </object-array>
</object-stream>"""

    XML_SESSION_TEMPLATE = """<object-stream>
  <map>
    <entry>
      <string>session</string>
      <org.bonitasoft.engine.session.impl.APISessionImpl>
        <id>{}</id>
        <creationDate>2017-09-07 09:45:39.844 UTC</creationDate>
        <duration>3600000</duration>
        <userName>{}</userName>
        <userId>{}</userId>
        <technicalUser>{}</technicalUser>
        <tenantName>default</tenantName>
        <tenantId>1</tenantId>
      </org.bonitasoft.engine.session.impl.APISessionImpl>
    </entry>
  </map>
</object-stream>"""

    API_IDENTITY = "org.bonitasoft.engine.api.IdentityAPI"
    API_BDM = "org.bonitasoft.engine.api.TenantAdministrationAPI"

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

    # Utils for server API

    def escapeXml(self, xml):
        return xml.replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace('\'','&apos;')

    def xmlSessionFromSession(self, session):
        xmlSession = BonitaClient.XML_SESSION_TEMPLATE.format(
            session['session_id'],
            session['user_name'],
            session['user_id'],
            session['is_technical_user'])
        return xmlSession

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
        r = self.getInternalSession().post( self.url + '/API/portal/page', data=payload, headers=headers)
        return self.formatResponse(r)

    def getPage(self, page_id):
        r = self.getInternalSession().get( self.url + '/API/portal/page/' + page_id)
        return self.formatResponse(r)

    def updatePage(self, page_id, server_filename):
        payload = json.dumps({'pageZip': server_filename})
        headers = { 'Content-Type': 'application/json' }
        r = self.getInternalSession().put( self.url + '/API/portal/page/' + page_id, data=payload, headers=headers)
        return self.formatResponse(r)

    # Application API

    def getApplications(self):
        params = {
            'o': 'id',
            'd': 'applicationId,pageId'
        }
        r = self.getInternalSession().get( self.url + '/API/living/application', params=params)
        return self.formatResponse(r)

    # Organization API

    def importOrganization(self, organizationFilename):
        rc, raw_session = self.getSession()
        session = json.loads(raw_session)
        xmlSession = self.xmlSessionFromSession(session)
        url  = self.url + "/serverAPI/" + BonitaClient.API_IDENTITY + "/" + "importOrganization"
        headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
        with open(organizationFilename, 'r') as organizationFile:
            data = organizationFile.read()
            escapedData = self.escapeXml(data)
            payload = {
                "options": xmlSession,
                "classNameParameters": BonitaClient.CLASSNAME_STRING_PARAMETER, 
                "parametersValues": BonitaClient.VALUE_STRING_PARAMETER.format( escapedData )
            }
            r = self.getInternalSession().post(url, data=payload, headers=headers)
            return self.formatResponse(r)
        return 'KO'

    def deleteOrganization(self):
        rc, raw_session = self.getSession()
        session = json.loads(raw_session)
        xmlSession = self.xmlSessionFromSession(session)
        payload = {
            "options": xmlSession,
            "classNameParameters": BonitaClient.CLASSNAME_VOID_PARAMETER,
            "parametersValues": BonitaClient.VALUE_NULL_PARAMETER
        }
        url  = self.url + "/serverAPI/" + BonitaClient.API_IDENTITY + "/" + "deleteOrganization"
        headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
        r = self.getInternalSession().post(url, data=payload, headers=headers)
        return self.formatResponse(r)

    def exportOrganization(self):
        rc, raw_session = self.getSession()
        xmlSession = self.xmlSessionFromSession(json.loads(raw_session))
        payload = {
            "options": xmlSession,
            "classNameParameters": BonitaClient.CLASSNAME_VOID_PARAMETER,
            "parametersValues": BonitaClient.VALUE_NULL_PARAMETER
        }
        url  = self.url + "/serverAPI/" + BonitaClient.API_IDENTITY + "/" + "exportOrganization"
        headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
        r = self.getInternalSession().post(url, data=payload, headers=headers)
        return self.formatResponse(r)

    # BDM API - Tenant Administration API  
    # Pause the tenant and restart it before use

    def installBusinessDataModel(self, zipFilename):
        rc, raw_session = self.getSession()
        session = json.loads(raw_session)
        xmlSession = self.xmlSessionFromSession(session)
        url  = self.url + "/serverAPI/" + BonitaClient.API_BDM + "/" + "installBusinessDataModel"
        headers = {}
        with open(zipFilename, 'rb') as zippedFile:
            zipDatas = zippedFile.read()
            javaarray = javaobj.JavaByteArray(zipDatas, classdesc=javaobj.ByteArrayDesc())
            datas = javaobj.dumps(javaarray)
            with open('/tmp/datas.ser', 'wb') as writefile:
                writefile.write(datas)
                writefile.close()
        files = {'binaryParameter0': ('binaryParameter0', open('/tmp/datas.ser','rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})}
        payload = {
            "options": xmlSession,
            "classNameParameters": BonitaClient.CLASSNAME_BINARY_PARAMETER,
            "parametersValues": BonitaClient.VALUE_BINARY_PARAMETER
        }
        r = self.getInternalSession().post(url, data=payload, files=files, headers=headers)
        return self.formatResponse(r)

    def uninstallBusinessDataModel(self):
        rc, raw_session = self.getSession()
        xmlSession = self.xmlSessionFromSession(json.loads(raw_session))
        payload = {
            "options": xmlSession,
            "classNameParameters": BonitaClient.CLASSNAME_VOID_PARAMETER,
            "parametersValues": BonitaClient.VALUE_NULL_PARAMETER
        }
        url  = self.url + "/serverAPI/" + BonitaClient.API_BDM + "/" + "uninstallBusinessDataModel"
        headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
        r = self.getInternalSession().post(url, data=payload, headers=headers)
        return self.formatResponse(r)

    def cleanAndUninstallBusinessDataModel(self):
        rc, raw_session = self.getSession()
        xmlSession = self.xmlSessionFromSession(json.loads(raw_session))
        payload = {
            "options": xmlSession,
            "classNameParameters": BonitaClient.CLASSNAME_VOID_PARAMETER,
            "parametersValues": BonitaClient.VALUE_NULL_PARAMETER
        }
        url  = self.url + "/serverAPI/" + BonitaClient.API_BDM + "/" + "cleanAndUninstallBusinessDataModel"
        headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
        r = self.getInternalSession().post(url, data=payload, headers=headers)
        return self.formatResponse(r)

    def getClientBDMZip(self, filename):
        rc, raw_session = self.getSession()
        xmlSession = self.xmlSessionFromSession(json.loads(raw_session))
        payload = {
            "options": xmlSession,
            "classNameParameters": BonitaClient.CLASSNAME_VOID_PARAMETER,
            "parametersValues": BonitaClient.VALUE_NULL_PARAMETER
        }
        url  = self.url + "/serverAPI/" + BonitaClient.API_BDM + "/" + "cleanAndUninstallBusinessDataModel"
        headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
        r = self.getInternalSession().post(url, data=payload, headers=headers, stream=True)
        content = r.content
        tarball_url = 'https://github.com/requests/requests/tarball/master'
        r = requests.get(tarball_url, stream=True)
        #byte[] getClientBDMZip()
        return self.formatResponse(r)

    def getBusinessDataModelVersion(self):
        rc, raw_session = self.getSession()
        xmlSession = self.xmlSessionFromSession(json.loads(raw_session))
        payload = {
            "options": xmlSession,
            "classNameParameters": BonitaClient.CLASSNAME_VOID_PARAMETER,
            "parametersValues": BonitaClient.VALUE_NULL_PARAMETER
        }
        url  = self.url + "/serverAPI/" + BonitaClient.API_BDM + "/" + "getBusinessDataModelVersion"
        headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
        r = self.getInternalSession().post(url, data=payload, headers=headers)
        return self.formatResponse(r)
