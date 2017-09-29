"""
bonita

Usage:
  bonita session [login <url> <username> <password>|logout|get]
  bonita system [tenant [get|pause|resume]]
  bonita platform [login <url> <username> <password>|logout|get|start|stop]
  bonita upload <type> <filename>
  bonita process [deploy <filename_on_server>|get [<process_id>]|enable <process_id>|disable <process_id>]
  bonita portal [page [deploy <filename_on_server>|get <page_id>|update <page_id> <filename_on_server>]]
  bonita application [get [<application_id>]|create <filename>|update <application_id> <filename>|delete <application_id>|import <server_filename>]
  bonita packaging [generate <dist_folder> <descriptor_file>|install <dist_folder> <descriptor_file>]
  bonita organization [import <filename>|export|delete]
  bonita bdm [install <filename>|uninstall|cleanAndUninstall|get [version|clientZip <filename>]]
  bonita profile [import <filename>|search [<criteria>]]
  bonita -h | --help
  bonita --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  bonita session login http://myhost:8080/bonita myusername mypassword
  bonita system tenant pause

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/rastaman/bonita-cli
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION

import inspect


def main():
    """Main CLI entrypoint."""
    import bonita.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():

        if hasattr(bonita.commands, k) and v:
            module = getattr(bonita.commands, k)
            bonita.commands = getmembers(module, isclass)
            command = [command[1] for command in bonita.commands if command[0] != 'Base' and inspect.getmodule(
                command[1]).__name__.startswith('bonita.commands')][0]
            command = command(options)
            command.run()
