# Ulto - Imperative Reversible Programming Language
#
# setup.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

import os
import platform
import sys
from pathlib import Path
from setuptools import setup, find_packages


class Setup:

    def __init__(self):
        print('+------------------------------------------------------+')
        print('|              Installing Ulto - v1.0.0                |')
        print('|               Developed By Aman Thapa Magar          |')
        print('+------------------------------------------------------+')
        print("| Operating System : " + platform.system())
        print("| Release          : " + platform.release())
        print("| Ulto Version     : v1.0.0                           |")

    def setup_link(self):
        """ Setup symbolic links or shortcuts based on the OS """
        if platform.system() == "Linux":
            print('| Unix-like install route                           |')
            self.unix_install_route()
        elif platform.system() == "Windows":
            print('| Windows install route                             |')
            self.windows_install_route()
        else:
            print('| Unsupported OS                                    |')
        print("+------------------------------------------------------+")

    def unix_install_route(self):
        """ Unix-like Install Route """
        bin_path = Path('/usr/local/bin/ulto')
        target_path = Path(__file__).resolve().parent / 'src' / 'main.py'

        if not bin_path.exists():
            bin_path.symlink_to(target_path)
            print(f"| Symbolic link created at {bin_path} -> {target_path}")
        else:
            print("| Symbolic link already exists at /usr/local/bin/ulto")

    def windows_install_route(self):
        """ Windows Install Route """
        try:
            import win32com.client
        except ImportError:
            print("pywin32 is required on Windows. Please install it using 'pip install pywin32'.")
            return

        shell = win32com.client.Dispatch('WScript.Shell')
        script_path = Path(__file__).resolve().parent / 'src' / 'main.py'
        link_path = Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Ultolink.lnk'

        if not link_path.exists():
            shortcut = shell.CreateShortCut(str(link_path))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{script_path}"'
            shortcut.WorkingDirectory = str(script_path.parent)
            shortcut.IconLocation = sys.executable
            shortcut.save()
            print(f"| Shortcut created at {link_path}")
        else:
            print(f"| Shortcut already exists at {link_path}")


if __name__ == "__main__":
    installer = Setup()
    installer.setup_link()

setup(
    name='ulto',
    version='1.0.0',
    author='Aman Thapa Magar',
    author_email='at719@sussex.ac.uk',
    description='Ulto - Imperative Reversible Programming Language',
    packages=find_packages(),
    install_requires=[
        'sortedcontainers',
        'pywin32; platform_system=="Windows"',
    ],
    entry_points={
        'console_scripts': [
            'ulto=src.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Programming Language :: Ulto :: 1',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={
        'src': ['operations.dll', 'liboperations.so'],
    },
    include_package_data=True,
)
