# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/cli.ipynb.

# %% auto 0
__all__ = ['StartProject', 'StartApp', 'LitManagementUtility', 'cli']

# %% ../nbs/cli.ipynb 3
import importlib
import os
from pathlib import Path
import sys

from django.core.management import ManagementUtility, execute_from_command_line, get_commands
from django.core.management.commands.startapp import Command as StartApp
from django.core.management.commands.startproject import Command as StartProject

from .utils import LITDJANGO_ROOT

# %% ../nbs/cli.ipynb 4
class StartProject(StartProject):

    rewrite_template_suffixes = (('.py-tpl', '.py'), (('.ipynb-tpl', '.ipynb')))

    def handle(self, **options):
        options["template"] = str(LITDJANGO_ROOT / "templates" / "project_template")
        options["extensions"] = ['py', 'txt', 'ipynb']
        super().handle(**options)

# %% ../nbs/cli.ipynb 5
class StartApp(StartApp):
    pass

# %% ../nbs/cli.ipynb 6
lit_commands = {
    "startapp": StartApp(),
    "startproject": StartProject()
}

# %% ../nbs/cli.ipynb 7
class LitManagementUtility(ManagementUtility):

    def __init__(self, argv=None):
        super().__init__(argv)

    def fetch_command(self, subcommand):
        """Use lit_commands version if it exists, otherwise fallback to django commands"""
        try: # find a lit_command version of the command
            return lit_commands[subcommand]
        except KeyError:
            # Fall back to default django  if we have not defined a custom command
            return super().fetch_command(subcommand)

# %% ../nbs/cli.ipynb 8
def cli():
    utility = LitManagementUtility(sys.argv)
    utility.execute()

