"""The session command."""


from json import dumps

from .base import Base

import os
import requests
import requests.utils
import pickle


class Session(Base):
    """Manage sessions"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        if self.options['login']:
            self.login()
        elif self.options['logout']:
            self.logout()
        elif self.options['show']:
            self.show()
        else:
            print("Nothing to do.")

    def login(self):
        url = self.options['<url>']
        username = self.options['<username>']
        password = self.options['<password>']

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
            #cookies.pop('JSESSIONID')
            configuration = self.loadConfiguration()
            configuration['url'] = url
            configuration['cookies'] = cookies
            self.saveConfiguration(configuration)
            print('OK')
        else:
            print('KO - %d' % r.status_code)

    def logout(self):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']
        session = requests.session()
        r = session.get( url + '/logoutservice', cookies=cookies)
        if r.status_code == 200:
            print('OK')
        else:
            print('KO - %d' % r.status_code)

    def show(self):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']
        session = requests.session()
        r = session.get( url + '/API/system/session/unusedid', cookies=cookies)
        if r.status_code == 200:
            print(r.text)
        else:
            print('KO - %d' % r.status_code)

