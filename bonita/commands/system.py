"""The system command."""

import os
import requests
import requests.utils
import pickle
import json

from .base import Base


class System(Base):
    """Manage system"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        if self.options['tenant']:
            if self.options['get']:
                self.getTenant()
            elif self.options['pause']:
                self.pauseTenant()
            elif self.options['resume']:
                self.resumeTenant()

    def getTenant(self):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']
        session = requests.session()
        r = session.get( url + '/API/system/tenant/unusedid', cookies=cookies)
        print(r.text)
    
    def isTenantPaused(self):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']
        session = requests.session()
        r = session.get( url + '/API/system/tenant/unusedid', cookies=cookies)
        response = json.loads(r.text)

    def pauseTenant(self):
        if not self.isTenantPaused():
            configuration = self.loadConfiguration()
            url = configuration['url']
            cookies = configuration['cookies']
            session = requests.session()
            payload = json.dumps({'paused': 'false'})
            print(cookies)
            r = session.put( url + '/API/system/tenant/unusedid', cookies=cookies, data=payload)
            if r.status_code == 200:
                print('OK')
            else:
                print r.text
                print r.status_code
                print('KO')
        else:
            print('OK')

    def resumeTenant(self):
        if self.isTenantPaused():
            configuration = self.loadConfiguration()
            url = configuration['url']
            cookies = configuration['cookies']
            session = requests.session()
            payload = json.dumps({'paused': 'true'})
            r = session.put( url + '/API/system/tenant/unusedid', cookies=cookies, data=payload, headers={
                'Content-Type': 'application/json'
            })
            if r.status_code == 200:
                print('OK')
            else:
                print r.text
                print r.status_code
                print('KO')
        else:
            print('OK')

    def toggleTenant(self, value):
        print('nope')
