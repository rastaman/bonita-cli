"""The portal command."""

from json import dumps
from .base import Base
from bonita.api.bonita_client import BonitaClient


class Portal(Base):

    """Manage portal"""

    def run(self):
        # bonita portal [page [deploy <filename_on_server>|get <page_id>|update <page_id> <filename_on_server>]]
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('deploy'):
            self.deploy()
        elif self.hasOption('get'):
            self.get()
        elif self.hasOption('update'):
            self.enable()
        else:
            print('Nothing to do.')

    def deploy(self):
        filename = self.options['<filename_on_server>']
        rc, datas = self.bonita_client.deployPage(filename)
        self.processResults(rc, datas)

    def get(self):
        page_id = self.options['<page_id>']
        rc, datas = self.bonita_client.getPage(page_id)
        self.processResults(rc, datas)

    def update(self):
        page_id = self.options['<page_id>']
        filename = self.options['<filename_on_server>']
        rc, datas = self.bonita_client.updatePage(page_id, filename)
        self.processResults(rc, datas)
