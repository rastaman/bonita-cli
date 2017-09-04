"""The system command."""

import requests
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
        else:
            print("Nothing to do.")

    def getTenant(self):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']
        session = requests.session()
        r = session.get( url + '/API/system/tenant/unusedid', cookies=cookies)
        print(r.text)

    def toggleTenantState(self, state):
        configuration = self.loadConfiguration()
        url = configuration['url']
        cookies = configuration['cookies']
        headers = {
            'X-Bonita-API-Token': configuration['token'],
            'Content-Type': 'application/json'
        }
        session = requests.session()
        payload = json.dumps({'paused': 'false'})
        r = session.put( url + '/API/system/tenant/unusedid', cookies=cookies, headers=headers, data=payload)
        if r.status_code == 200:
            print('OK')
        else:
            print r.text
            print r.status_code
            print('KO')

    def pauseTenant(self):
        self.toggleTenantState('false')

    def resumeTenant(self):
        self.toggleTenantState('true')
