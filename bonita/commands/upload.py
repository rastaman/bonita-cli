"""The upload command."""


from json import dumps

from .base import Base

import os
import requests


class Upload(Base):
    """Manage uploads"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        if self.options['upload']:
            self.upload()
# /portal/fileUpload, supports any type of files
# /portal/processUpload, supports only .bar files
# /portal/organizationUpload, supports only .xml files
# /portal/actorsUpload, supports only .xml files
# /portal/imageUpload, supports only .png, .jpg, .gif, .jpeg, .bmp, .wbmp or .tga files
# /portal/pageUpload, supports only .zip files
# /portal/applicationsUpload, supports only .xml files
# /portal/connectorImplementation, supports only .zip files (not available in Community edition)
# /portal/reportUpload, supports any type of file (not available in Community edition)
# /portal/resourceUpload, supports only .jar files (not available in Community edition)
# /portal/profilesUpload, supports only .xml files (not available in Community edition)

    def upload(self):
        type = self.options['<type>']
        filename = self.options['<filename>']
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']

        files = {'file': open(filename, 'rb')}
        r = requests.post(url + '/portal/' + type + 'Upload', files=files, cookies=cookies)
        if r.status_code == 200:
            print('OK')
        else:
            print('KO - %d' % r.status_code)
            print(r.text)
