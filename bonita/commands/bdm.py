"""The bdm command."""

from json import dumps
from .base import Base
from bonita.api.bonita_client import BonitaClient


class BDM(Base):
    
    """Manage Business Data Model"""

    def run(self):
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        #bonita organization [import <filename>|export|delete]
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('install'):
            self.install()
        elif self.hasOption('uninstall'):
            self.uninstall()
        elif self.hasOption('cleanAndUninstall'):
            self.cleanAndUninstall()
        elif self.hasOption('get'):
            self.get()
        else:
            print('Nothing to do.')

    def install(self):
        filename = self.options['<filename>']
        rc, datas = self.bonita_client.installBusinessDataModel(filename)
        self.processResults(rc, datas)

    def uninstall(self):
        rc, datas = self.bonita_client.uninstallBusinessDataModel()
        self.processResults(rc, datas)

    def cleanAndUninstall(self):
        rc, datas = self.bonita_client.cleanAndUninstallBusinessDataModel()
        self.processResultCode(rc)

    def get(self):
        if self.hasOption('version'):
            rc, datas = self.bonita_client.getBusinessDataModelVersion()
            self.processResults(rc, datas)
        elif self.hasOption('clientZip'):
            filename = self.options['filename']
            rc, datas = self.bonita_client.getClientBDMZip(filename)
            self.processResults(rc, datas)

