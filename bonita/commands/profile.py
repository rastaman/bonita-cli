"""The Profile command."""

from .base import Base
from bonita.api.bonita_client import BonitaClient


class Profile(Base):

    """Manage Profile"""

    def run(self):
        #from json import dumps
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('import'):
            self.importProfiles()
        elif self.hasOption('search'):
            self.searchProfiles()
        else:
            print('Nothing to do.')

    def importProfiles(self):
        filename = self.options['<filename>']
        rc, datas = self.bonita_client.importProfiles(filename)
        self.processResults(rc, datas)

    def searchProfiles(self):
        criteria = self.options['<criteria>']
        rc, datas = self.bonita_client.searchProfiles(criteria)
        self.processResults(rc, datas)
