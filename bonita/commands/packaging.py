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
        elif self.hasOption('install'):
            self.installDescriptor()
        else:
            print('Nothing to do.')

    def generateDescriptor(self):
        dist_folder = self.options['<dist_folder>']
        descriptor_file = self.options['<descriptor_file>']
        rc = self.bonita_client.generateDescriptor(
            dist_folder, descriptor_file)
        self.processResultCode(rc)

    def installDescriptor(self):
        dist_folder = self.options['<dist_folder>']
        descriptor_file = self.options['<descriptor_file>']
        rc = self.bonita_client.installDescriptor(
            dist_folder, descriptor_file)
        self.processResultCode(rc)
