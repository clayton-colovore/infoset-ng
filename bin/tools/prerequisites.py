#!/usr/bin/env python3
"""Infoset  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys
import getpass
import subprocess


def main():
    """Run basic tests.

    Args:
        None

    Returns:
        None

    """
    # Test validity
    version = _Version()
    version.version()


class _Version(object):
    """Class to test setup."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.username = getpass.getuser()

    def version(self):
        """Determine versions.

        Args:
            None

        Returns:
            None

        """
        # Run tests
        valid_list = [self._python(), self._mysql()]
        if False not in valid_list:
            # Setup the log message
            if self.username == 'root':
                flag = ''
                prompt = '#'
            else:
                flag = '--user '
                prompt = '$'
            log_message = ("""\

------------------------------------------------------------------

Run the following command to setup libraries prior to installation.

{} pip3 install {}sqlalchemy yaml
""".format(prompt, flag))
            print(log_message)

    def _python(self):
        """Determine Python version.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        valid = True
        major = 3
        minor = 5
        major_installed = sys.version_info[0]
        minor_installed = sys.version_info[1]

        # Exit if python version is too low
        if major_installed < major:
            valid = False
        elif major_installed == major and minor_installed < minor:
            valid = False
        if valid is False:
            log_message = (
                'Required python version must be >= {}.{}. '
                'Python version {}.{} installed'
                ''.format(major, minor, major_installed, minor_installed))
            print(log_message)
        else:
            log_message = (
                '\nPython version {}.{} OK'
                ''.format(major_installed, minor_installed))
            print(log_message)

        # Return
        return valid

    def _mysql(self):
        """Determine MySQL version.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        valid = True
        versions = {
            'maria': {'major': 10, 'minor': 0},
            'mysql': {'major': 5, 'minor': 7}
        }

        # Get response from mysql command
        cli_string = '/usr/bin/mysql --version'
        response = _run_script(cli_string)

        # Not OK if not fount
        if response['error_code'] != 0:
            valid = False
            log_message = ('MySQL / MariaDB not installed.')
            print(log_message)
        else:
            # Determine major and minor versions of software
            version_string = response['output'].split()[4]
            version_list = version_string.split('.')
            major_installed = int(version_list[0])
            minor_installed = int(version_list[1])

            # We are running MariaDB
            if 'maria' in version_string.lower():
                major = versions['maria']['major']
                minor = versions['maria']['minor']

                # Exit if  version is too low
                if major_installed < major:
                    valid = False
                elif major_installed == major and minor_installed < minor:
                    valid = False
                else:
                    valid = True

                if valid is False:
                    log_message = (
                        'MariaDB version needs to be >= than {}.{}.'
                        ''.format(major, minor))
                    print(log_message)
                else:
                    log_message = (
                        'MariaDB version {}.{} OK'
                        ''.format(major_installed, minor_installed))
                    print(log_message)

            # We are running MySQL
            else:
                major = versions['mysql']['major']
                minor = versions['mysql']['minor']

                # Exit if  version is too low
                if major_installed < major:
                    valid = False
                elif major_installed == major and minor_installed < minor:
                    valid = False
                else:
                    valid = True

                if valid is False:
                    log_message = (
                        'MySQL version needs to be >= than {}.{}.'
                        ''.format(major, minor))
                    print(log_message)
                else:
                    log_message = (
                        'MySQL version {}.{} OK'
                        ''.format(major_installed, minor_installed))
                    print(log_message)

        # Return
        return valid


def _run_script(cli_string, shell=False):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        cli_string: Command to run on the CLI
        die: Die if command runs with an error

    Returns:
        None

    """
    # Initialize key variables
    data = {}

    # Create the subprocess object
    if shell is False:
        do_command_list = list(cli_string.split(' '))
        process = subprocess.Popen(
            do_command_list,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(
            cli_string,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    stdoutdata, _ = process.communicate()
    returncode = process.returncode

    # Return
    data = {
        'output': stdoutdata.decode(),
        'error_code': returncode
    }
    return data


if __name__ == '__main__':
    # Run main
    main()
