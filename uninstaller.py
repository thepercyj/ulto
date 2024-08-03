# Ulto - Imperative Reversible Programming Language
#
# uninstaller.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>


import os


def remove_link():
    if os.name == 'posix':
        bin_path = '/usr/local/bin/ulto'
        if os.path.exists(bin_path):
            os.remove(bin_path)
            print(f"Removed symbolic link at {bin_path}")
    elif os.name == 'nt':
        link_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs',
                                 'Ultolink.lnk')
        if os.path.exists(link_path):
            os.remove(link_path)
            print(f"Removed shortcut at {link_path}")


def uninstall_package(package_name):
    os.system(f"pip uninstall -y {package_name}")


if __name__ == '__main__':
    package_name = 'ulto'
    uninstall_package(package_name)
    remove_link()
