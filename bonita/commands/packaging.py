"""The Packaging command."""

from .base import Base
from bonita.api.bonita_client import BonitaClient


class Packaging(Base):

    """Manage Packaging"""

    def run(self):
        #from json import dumps
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('generate'):
            self.generateDescriptor()
        else:
            print('Nothing to do.')

    def generateDescriptor(self):
        dist_folder = self.options['<dist_folder>']
        descriptor_file = self.options['<descriptor_file>']
        rc, datas = self.bonita_client.generateDescriptor(
            dist_folder, descriptor_file)
        self.processResults(rc, datas)