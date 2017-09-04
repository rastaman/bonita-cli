"""The system command."""

from .base import Base
from bonita.api.bonita_client import BonitaClient


class System(Base):
    """Manage system"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
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
        rc, datas = self.bonita_client.getCurrentTenant()
        if rc == 200:
            print(datas)
        else:
            print('KO - %d', rc)

    def toggleTenantState(self, state):
        rc = self.bonita_client.toggleTenantState(state)
        if rc == 200:
            print('OK')
        else:
            print('KO - %d' % rc)

    def pauseTenant(self):
        self.toggleTenantState('true')

    def resumeTenant(self):
        self.toggleTenantState('false')
