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
        elif self.hasOption('export'):
            self.exportProfiles()
        elif self.hasOption('merge'):
            self.mergeProfiles()
        elif self.hasOption('search'):
            self.searchProfiles()
        else:
            print('Nothing to do.')

    def importProfiles(self):
        filename = self.options['<filename>']
        rc, datas = self.bonita_client.importProfiles(filename)
        self.processResults(rc, datas)

    def exportProfiles(self):
        filename = self.options['<filename>']
        rc, datas = self.bonita_client.exportProfiles(filename)
        self.processResults(rc, datas)

    def mergeProfiles(self):
        default_profiles = self.options['<default_profiles>']
        custom_profiles = self.options['<custom_profiles>']
        output_profiles = self.options['<output_profiles>']
        rc = self.bonita_client.mergeProfiles(default_profiles, custom_profiles, output_profiles)
        self.processResultCode(rc)

    def searchProfiles(self):
        criteria = self.options['<criteria>']
        rc, datas = self.bonita_client.searchProfiles(criteria)
        self.processResults(rc, datas)
