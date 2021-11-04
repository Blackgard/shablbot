"""
Shablbot manager commands
"""

import sys


def main():
    try:
        from shablbot.core.manager_commands import manager_command
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Shablbot. Are you sure it's installed and activate venv?"
        ) from exc
    manager_command(sys.argv)


if __name__ == '__main__':
    main()
