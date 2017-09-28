"""The application command."""

from json import dumps
from .base import Base
from bonita.api.bonita_client import BonitaClient
from wsgiref.util import application_uri


class Application(Base):

    """Manage application"""

    def run(self):
        # bonita application [get <application_id>]
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.get()
        elif self.hasOption('create'):
            self.create()
        elif self.hasOption('update'):
            self.update()
        elif self.hasOption('delete'):
            self.delete()
        elif self.hasOption('import'):
            self.importApplication()
        else:
            print('Nothing to do.')

    def get(self):
        application_id = self.options['<application_id>']
        if application_id is None:
            rc, datas = self.bonita_client.getApplications()
            self.processResults(rc, datas)
        else:
            rc, datas = self.bonita_client.getApplication(application_id)
            self.processResults(rc, datas)

    def create(self):
        filename = self.options['<filename>']
        rc, datas = self.bonita_client.createApplication(filename)
        self.processResults(rc, datas)

    def update(self):
        application_id = self.options['<application_id>']
        filename = self.options['<filename>']
        rc, datas = self.bonita_client.updateApplication(
            application_id, filename)
        self.processResults(rc, datas)

    def delete(self):
        application_id = self.options['<application_id>']
        rc, datas = self.bonita_client.deleteApplication(application_id)
        self.processResults(rc, datas)

    def importApplication(self):
        server_filename = self.options['<server_filename>']
        rc, datas = self.bonita_client.importApplication(server_filename)
        self.processResults(rc, datas)
