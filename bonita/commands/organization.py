"""The organization command."""

from json import dumps
from .base import Base
from bonita.api.bonita_client import BonitaClient


class Organization(Base):
    
    """Manage organization"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        #bonita organization [import <filename>|get <organization_id>|export <organization_id>|delete]
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('import'):
            self.importOrganization()
        elif self.hasOption('export'):
            self.exportOrganization()
        elif self.hasOption('get'):
            self.get()
        elif self.hasOption('delete'):
            self.delete()
        else:
            print('Nothing to do.')

    def importOrganization(self):
        filename = self.options['<filename>']
        rc, datas = self.bonita_client.importOrganization(filename)
        self.processResults(rc, datas)

    def get(self):
        organization_id = self.options['<organization_id>']
        rc, datas = self.bonita_client.getOrganization(organization_id)
        self.processResults(rc, datas)

    def exportOrganization(self):
        organization_id = self.options['<organization_id>']
        rc, datas = self.bonita_client.exportOrganization(organization_id)
        self.processResults(rc, datas)

    def delete(self):
        rc, datas = self.bonita_client.deleteOrganization()
        self.processResultCode(rc)
