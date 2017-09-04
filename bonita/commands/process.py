"""The process command."""

from json import dumps
from .base import Base
from bonita.api.bonita_client import BonitaClient


class Process(Base):
    
    """Manage process"""

    def run(self):
        #bonita process [deploy <filename_on_server>|get <process_id>|enable <process_id>|disable <process_id>]
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.options['deploy']:
            self.deploy()
        elif self.options['get']:
            self.get()
        elif self.options['enable']:
            self.enable()
        elif self.options['disable']:
            self.disable()
        else:
            print('Nothing to do.')

    def deploy(self):
        filename = self.options['<filename_on_server>']

        rc, datas = self.bonita_client.deployProcess(filename)

        if rc == 200:
            print(datas)
        else:
            print('KO - %d' % rc)

    def get(self):
        process_id = self.options['<process_id>']

        rc, datas = self.bonita_client.getProcess(process_id)

        if rc == 200:
            print(datas)
        else:
            print('KO - %d' % rc)

    def enable(self):
        process_id = self.options['<process_id>']

        rc, datas = self.bonita_client.enableProcess(process_id)

        if rc == 200:
            print(datas)
        else:
            print('KO - %d - %s' % (rc, datas) )

    def disable(self):
        process_id = self.options['<process_id>']

        rc, datas = self.bonita_client.disableProcess(process_id)

        if rc == 200:
            print(datas)
        else:
            print('KO - %d' % rc)
