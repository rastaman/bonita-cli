"""The platform command."""

import requests
import requests.utils
import json

from .base import Base


class Platform(Base):
    """Manage platform"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        if self.options['login']:
            self.login()
        elif self.options['start']:
            self.start()
        elif self.options['stop']:
            self.stop()
        elif self.options['get']:
            self.get()
        elif self.options['logout']:
            self.logout()
        else:
            print('Nothing to do.')

    def login(self):
        url = self.options['<url>']
        username = self.options['<username>']
        password = self.options['<password>']

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
            #cookies.pop('JSESSIONID')

            configuration = self.loadConfiguration()
            configuration['url'] = url
            configuration['platform_cookies'] = cookies
            self.saveConfiguration(configuration)
            print('OK')
        else:
            print('KO - %d' % r.status_code)
            print(r.text)

    def logout(self):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['platform_cookies']
        session = requests.session()
        r = session.get( url + '/platformlogoutservice?redirect=false', cookies=cookies)
        if r.status_code == 200:
            print('OK')
        else:
            print('KO - %d' % r.status_code)

    def get(self):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['platform_cookies']
        r = requests.get( url + '/API/platform/platform/unusedid', cookies=cookies)
        response = json.loads(r.text)
        print(json.dumps(response, indent=True))

    def toggleState(self, state):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['platform_cookies']
        payload = json.dumps({'state': state})
        r = requests.put( url + '/API/platform/platform/unusedid', cookies=cookies, data=payload, headers={
            'Content-Type': 'application/json'
        })
        if r.status_code == 200:
            print('OK')
        else:
            print r.text
            print r.status_code
            print('KO')

    def start(self):
        self.toggleState('start')

    def stop(self):
        self.toggleState('stop')
