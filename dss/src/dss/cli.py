import sys
import os
from pathlib import Path
from dss.generator import DjangoProjectGenerator


def show_help():
    print("Django Simple Starter CLI")
    print("")
    print("Usage:")
    print("  dss <project_name>    Create a new Django project")
    print("  dss --help            Show this help message")
    print("")
    print("After installing django-simple-starter, create a project:")
    print("  dss my_project")
    print("")
    print("Then follow the instructions shown to set up your project.")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        show_help()
        sys.exit(0)

    project_name = sys.argv[1].strip()

    if not project_name:
        print("Error: Project name cannot be empty.")
        sys.exit(1)

    generator = DjangoProjectGenerator(project_name)
    generator.generate()