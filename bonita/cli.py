"""
bonita

Usage:
  bonita hello
  bonita session [login <url> <username> <password>|logout|show]
  bonita upload <type> <file>
  bonita system [tenant [get|pause|resume]]
  bonita -h | --help
  bonita --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  bonita hello
  bonita session --action=login --username=install --password=install

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/rastaman/bonita-cli
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


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
            command = [command[1] for command in bonita.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
