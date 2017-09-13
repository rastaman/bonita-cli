"""The Profile command."""

from json import dumps
from .base import Base
from bonita.api.bonita_client import BonitaClient


class Profile(Base):
    
    """Manage Profile"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        #bonita Profile [import <filename>|export|delete]
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('import'):
            self.importProfile()
        elif self.hasOption('export'):
            self.exportProfile()
        else:
            print('Nothing to do.')

    def importProfile(self):
        filename = self.options['<filename>']
        rc, datas = self.bonita_client.importProfile(filename)
        self.processResults(rc, datas)

    def exportProfile(self):
        rc, datas = self.bonita_client.exportProfile()
        self.processResults(rc, datas)

