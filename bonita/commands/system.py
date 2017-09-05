"""The system command."""

from .base import Base
from bonita.api.bonita_client import BonitaClient


class System(Base):
    """Manage system"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('tenant'):
            if self.hasOption('get'):
                self.getTenant()
            elif self.hasOption('pause'):
                self.pauseTenant()
            elif self.hasOption('resume'):
                self.resumeTenant()
        else:
            print("Nothing to do.")

    def getTenant(self):
        rc, datas = self.bonita_client.getCurrentTenant()
        self.processResults(rc, datas)

    def toggleTenantState(self, state):
        rc = self.bonita_client.toggleTenantState(state)
        self.processResultCode(rc)

    def pauseTenant(self):
        self.toggleTenantState('true')

    def resumeTenant(self):
        self.toggleTenantState('false')
