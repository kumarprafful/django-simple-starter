import sys
import os
from pathlib import Path
from dss.generator import DjangoProjectGenerator


def main():
    if len(sys.argv) < 2:
        project_name = input("Enter project name: ").strip()
    else:
        project_name = sys.argv[1].strip()

    if not project_name:
        print("Error: Project name cannot be empty.")
        sys.exit(1)

    generator = DjangoProjectGenerator(project_name)
    generator.generate()