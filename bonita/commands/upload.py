"""The upload command."""


from json import dumps

from .base import Base

import os
import requests
from wheel.test.test_ranking import sup

SUPPORTED_TYPES = {
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

class Upload(Base):
    """Manage uploads"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        if self.options['upload']:
            self.upload()

    def upload(self):
        uploadType = self.options['<type>']
        if uploadType not in SUPPORTED_TYPES:
            print('Unsupported upload type: %s' % uploadType)
            return
        filename,extension = os.path.splitext(self.options['<filename>'])
        if len(SUPPORTED_TYPES.get(uploadType)) != 0 and not extension in SUPPORTED_TYPES.get(uploadType):
            print('Unsupported extension %s for upload type %s (supported: %s)' % (extension, uploadType, SUPPORTED_TYPES.get(uploadType)))
            return
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']
        headers = { 'X-Bonita-API-Token': configuration['token'] }
        files = {'file': open(filename + extension, 'rb')}
        r = requests.post(url + '/portal/' + uploadType + 'Upload', files=files, headers=headers, cookies=cookies)
        if r.status_code == 200:
            print('OK')
            print(r.text)
        else:
            print('KO - %d' % r.status_code)
            print(r.text)
