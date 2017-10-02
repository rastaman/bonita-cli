"""The user command."""

from json import dumps
from .base import Base
from bonita.api.bonita_client import BonitaClient


class User(Base):

    """Manage user"""

    def run(self):
        # bonita process [deploy <filename_on_server>|get <process_id>|enable <process_id>|disable <process_id>]
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('add'):
            self.add()
        #if self.hasOption('update'):
        #    self.add()
        elif self.hasOption('get'):
            self.get()
        elif self.hasOption('remove'):
            self.remove()
        elif self.hasOption('enable'):
            self.enable()
        elif self.hasOption('disable'):
            self.disable()
        else:
            print('Nothing to do.')

    def add(self):
        payload = {
            'userName':self.getOption("<login>"),
            'password':self.getOption("<password>"),
            'password_confirm':self.getOption("<password>"),
            'icon':self.getOption("<icon>",""),
            'firstName':self.getOption("<firstName>",""),
            'lastName':self.getOption("<lastName>",""),
            'title':self.getOption("<title>",""),
            'job_title':self.getOption("<job_title>",""),
            'manager_id':self.getOption("<manager_id>",0)
        }
        rc, datas = self.bonita_client.addUser(payload)
        self.processResults(rc, datas)

    def get(self):
        if self.hasOption('<user_id>'):
            user_id = self.options['<user_id>']
            rc, datas = self.bonita_client.getUser(user_id)
            self.processResults(rc, datas)
        else:
            rc, datas = self.bonita_client.getUsers()
            self.processResults(rc, datas)

    def remove(self):
        if self.hasOption('<user_id>'):
            user_id = self.options['<user_id>']
            rc, datas = self.bonita_client.deleteUser(user_id)
            self.processResults(rc, datas)

    def enable(self):
        user_id = self.options['<user_id>']
        rc, datas = self.bonita_client.enableUser(user_id)
        self.processResults(rc, datas)

    def disable(self):
        user_id = self.options['<user_id>']
        rc, datas = self.bonita_client.disableUser(user_id)
        self.processResults(rc, datas)
