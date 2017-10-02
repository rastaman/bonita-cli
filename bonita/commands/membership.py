"""The membership command."""

from json import dumps
from .base import Base
from bonita.api.bonita_client import BonitaClient


class Membership(Base):

    """Manage membership"""

    def run(self):
        self.bonita_client = BonitaClient(self.loadConfiguration())
        if self.hasOption('add'):
            self.add()
        elif self.hasOption('get'):
            self.get()
        elif self.hasOption('remove'):
            self.remove()
#        elif self.hasOption('update'):
#            self.update()
#        elif self.hasOption('remove'):
#            self.remove()
        else:
            print('Nothing to do.')

    def add(self):
        payload = {
            'user_id': self.options['<user_id>'],
            'group_id': self.options['<group_id>'],
            'role_id': self.options['<role_id>']
        }
        rc, datas = self.bonita_client.addMembership(payload)
        return self.processResults(rc, datas)

    def get(self):
        user_id = self.options['<user_id>']
        rc, datas = self.bonita_client.getMemberships(user_id)
        return self.processResults(rc, datas)

    # Delete a membership of a user using the group id and role id.#
    def remove(self):
        payload = {
            'user_id': self.options['<user_id>'],
            'group_id': self.options['<group_id>'],
            'role_id': self.options['<role_id>']
        }
        rc, datas = self.bonita_client.removeMembership(payload)
        return self.processResults(rc, datas)

#DELETE
#    def update(self):
#        page_id = self.options['<page_id>']
#        filename = self.options['<filename_on_server>']
#        rc, datas = self.bonita_client.updateMembership(page_id, filename)
#        self.processResults(rc, datas)
