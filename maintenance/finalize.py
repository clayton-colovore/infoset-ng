#!/usr/bin/env python3
"""infoset  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys
import getpass
import os


# Try to create a working PYTHONPATH
_MAINT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(
    os.path.join(_MAINT_DIRECTORY, os.pardir))
if _ROOT_DIRECTORY.endswith('/infoset-ng') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'Infoset-NG is not installed in a "infoset-ng/" directory. '
        'Please fix.')
    sys.exit(2)

# Copy configuration file from examples directory if it doesn't already exist

# Do infoset-ng imports
from infoset.utils import log
from maintenance import misc
from infoset.utils import general
from infoset.utils import daemon as daemon_lib


def run():
    """Do the installation.

    Args:
        None

    Returns:
        None

    """
    # Prevent running as sudo user
    if 'SUDO_UID' in os.environ:
        log_message = (
            'Cannot run installation using "sudo". Run as a regular user to '
            'install in this directory or as user "root".')
        log.log2die_safe(1029, log_message)

    # Start daemons
    daemon = _Daemon()
    daemon.start()

    # Run the post check
    postcheck = _PostCheck()
    postcheck.validate()


class _Daemon(object):
    """Class to start infoset-ng daemons."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """

    def start(self):
        """Write the config to file.

        Args:
            None


        Returns:
            None
        """
        # Get daemon status
        daemons = ['infoset-ng-api', 'infoset-ng-ingester']
        for daemon in daemons:
            # Initialize key variables
            success = False
            running = self._running(daemon)

            # Prompt to restart if already running
            if running is True:
                restart = input(
                    '\nINPUT - Daemon {} is running. Restart? [Y/n] '
                    ''.format(daemon))
                if bool(restart) is False:
                    success = self._restart(daemon)
                    if success is True:
                        misc.print_ok(
                            'Successfully restarted daemon {}.'.format(daemon))
                elif restart[0].lower() != 'n':
                    success = self._restart(daemon)
                    if success is True:
                        misc.print_ok(
                            'Successfully restarted daemon {}.'.format(daemon))
                else:
                    misc.print_ok(
                        'Leaving daemon {} unchanged.'.format(daemon))
                    success = True
            else:
                success = self._start(daemon)
                if success is True:
                    misc.print_ok(
                        'Successfully started daemon {}.'.format(daemon))

            # Message if no success
            if success is False:
                log_message = ('Failed to start daemon {}.'.format(daemon))
                log.log2see_safe(1008, log_message)

    def _restart(self, daemon):
        """Start or restart daemon.

        Args:
            daemon: Name of daemon

        Returns:
            None

        """
        # restart
        return self._start(daemon, restart=True)

    def _start(self, daemon, restart=False):
        """Start or restart daemon.

        Args:
            daemon: Name of daemon
            restart: Restart if True

        Returns:
            None

        """
        # Initialize key variables
        username = getpass.getuser()
        running = False
        if restart is True:
            attempt = 'restart'
        else:
            attempt = 'start'

        # Get status
        root_directory = general.root_directory()
        if restart is False:
            if username == 'root':
                script_name = (
                    '/bin/systemctl start {}.service'.format(daemon))
            else:
                script_name = (
                    '{}/bin/{} --start'.format(root_directory, daemon))
        else:
            if username == 'root':
                script_name = (
                    '/bin/systemctl restart {}.service'.format(daemon))
            else:
                script_name = (
                    '{}/bin/{} --restart --force'
                    ''.format(root_directory, daemon))

        # Attempt to restart / start
        response = general.run_script(script_name, die=False)
        if bool(response['returncode']) is True:
            log_message = ('Could not {} daemon {}.'.format(attempt, daemon))
            log.log2see_safe(1012, log_message)

        # Return after waiting for daemons to startup properly
        running = self._running(daemon)
        return running

    def _running(self, daemon):
        """Determine status of daemon.

        Args:
            daemon: Name of daemon

        Returns:
            running: True if running

        """
        # Initialize key variables
        running = False

        # Get status of file (Don't create directories)
        if daemon_lib.pid_file_exists(daemon) is True:
            running = True

        # Return
        return running


class _PostCheck(object):
    """Class to test post setup."""

    def __init__(self):
        """Method for intializing the class.

        Args:
            None

        Returns:
            None

        """

    def validate(self):
        """Validate .

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        username = getpass.getuser()
        suggestions = ''
        line = '*' * 80

        #######################################################################
        # Give suggestions as to what to do
        #
        # NOTE!
        #
        # The root user should only use the systemctl commands as the daemons
        # could be running as another user and lock and pid files will be owned
        # by that user. We don't want the daemons to crash at some other time
        # because these files are owned by root with denied delete privileges
        #######################################################################
        if username != 'root':
            suggestions = (
                'Infoset-NG will not automatically restart after a reboot. '
                'You need to re-install as the "root" user for this to occur.'
            )
            print('{}\n{}\n{}'.format(line, suggestions, line))

        # All done
        misc.print_ok(
            'Installation complete, pending changes mentioned above.')


def _pip3_install(module):
    """Install python module using pip3.

    Args:
        module: module to install

    Returns:
        None

    """
    # Find pip3 executable
    cli_string = 'which pip3'
    response = general.run_script(cli_string, die=False)

    # Not OK if not fount
    if bool(response['returncode']) is True:
        log_message = ('python pip3 not installed.')
        log.log2die_safe(1041, log_message)
    else:
        log_message = 'Python pip3 executable found.'
        misc.print_ok(log_message)

    # Determine version of pip3
    cli_string = 'pip3 --version'
    _response = os.popen(cli_string).read()
    version = _response.split()[1]

    # Attempt to install module
    if version < '9.0.0':
        cli_string = 'pip3 list | grep {}'.format(module)
    else:
        cli_string = 'pip3 list --format columns | grep {}'.format(module)
    __response = bool(os.popen(cli_string).read())

    if __response is False:
        # YAML is not installed try to install it
        cli_string = 'pip3 install --user {}'.format(module)
        response_install = general.run_script(cli_string, die=False)

        # Fail if module cannot be installed
        if bool(response_install['returncode']) is True:
            log_message = ('python pip3 cannot install "{}".'.format(module))
            log.log2die_safe(1100, log_message)
        else:
            log_message = (
                'Python module "{}" is installed.'.format(module))
            misc.print_ok(log_message)
    else:
        log_message = 'Python module "{}" is installed.'.format(module)
        misc.print_ok(log_message)


if __name__ == '__main__':
    # Run main
    run()
