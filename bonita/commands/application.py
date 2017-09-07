"""The application command."""

from json import dumps
from .base import Base
from bonita.api.bonita_client import BonitaClient


class Application(Base):
    
    """Manage application"""

    def run(self):
        #bonita application [get <application_id>]
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.get()
        #elif self.hasOption('get'):
        #    self.get()
        #elif self.hasOption('update'):
        #    self.enable()
        else:
            print('Nothing to do.')

    def get(self):
        application_id = self.options['<application_id>']
        if application_id is None:
            rc, datas = self.bonita_client.getApplications()
            self.processResults(rc, datas)

