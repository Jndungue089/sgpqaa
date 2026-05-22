#!/usr/bin/env python3
"""Atalho de gestão Django a partir da raiz do workspace."""
import os
import sys
from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parent / 'sgpqaa'
    sys.path.insert(0, str(project_root))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgpqaa.settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
