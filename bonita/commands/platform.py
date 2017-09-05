"""The platform command."""

from .base import Base
from bonita.api.bonita_client import BonitaClient


class Platform(Base):
    """Manage platform"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOptions('login'):
            self.login()
        elif self.hasOption('start'):
            self.start()
        elif self.hasOption('stop'):
            self.stop()
        elif self.hasOption('get'):
            self.get()
        elif self.hasOption('logout'):
            self.logout()
        else:
            print('Nothing to do.')

    def login(self):
        url = self.options['<url>']
        username = self.options['<username>']
        password = self.options['<password>']

        rc = self.bonita_client.platformLogin(url, username, password)
        
        if rc == 200:
            self.saveConfiguration(self.bonita_client.getConfiguration())
        self.processResultCode(rc)

    def logout(self):
        rc = self.bonita_client.platformLogout()
        self.processResultCode(rc)

    def get(self):
        rc, datas = self.bonita_client.getPlatform()
        self.processResults(rc, datas)

    def start(self):
        rc = self.bonita_client.togglePlatformState('start')
        self.processResultCode(rc)

    def stop(self):
        rc = self.bonita_client.togglePlatformState('stop')
        self.processResultCode(rc)
