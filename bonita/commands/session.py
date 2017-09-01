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
            print("No supported action found.")

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

        configuration = {
            'url': url,
            'cookies': requests.utils.dict_from_cookiejar(r.cookies)
        }
        self.saveConfiguration(configuration)

    def logout(self):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']
        session = requests.session()
        r = session.get( url + '/logoutservice', cookies=cookies)
        if r.status_code == 200:
            print('OK')
        else:
            print ('KO')

    def show(self):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']
        session = requests.session()
        r = session.get( url + '/API/system/session/unusedid', cookies=cookies)
        print(r.text)
