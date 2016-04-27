"""This modules defines a L3 router class, with a modulable config system."""
from ipmininet import DEBUG_FLAG
from ipmininet.utils import L3Router
from .config import BasicRouterConfig

from mininet.node import Node


class ProcessHelper(object):
    """This class holds processes that are part of a given family, e.g. routing
    daemons. This also provides the abstraction to execute a new process,
    currently in a mininet namespace, but could be extended to execute in
    a different environment."""

    def __init__(self, node, *args, **kwargs):
        """:param node: The object to use to create subprocesses."""
        self.node = node
        self._pid_gen = 0
        self._processes = {}
        super(ProcessHelper, self).__init__(*args, **kwargs)

    def call(self, *args, **kwargs):
        """Call a command, wait for it to end and return its ouput.

        :param args: the command + arguments
        :param kwargs: key-val arguments, as used in subprocess.Popen"""
        return self.node.cmd(*args, **kwargs)

    def popen(self, *args, **kwargs):
        """Call a command and return a Popen handle to it.

        :param args: the command + arguments
        :param kwargs: key-val arguments, as used in subprocess.Popen
        :return: a process index in this family"""
        self._pid_gen += 1
        self._processes[self._pid_gen] = self.node.popen(*args, **kwargs)
        return self._pid_gen

    def get_process(self, pid):
        """Return a given process handle in this family

        :param pid: a process index, as return by popen"""
        return self._processes[pid]

    def terminate(self):
        """Terminate all processes in this family"""
        for p in self._processes.itervalues():
            try:
                p.terminate()
            except OSError:
                pass  # Process is already dead


class Router(Node, L3Router):
    """The actualy router, which manages a set of daemons"""

    def __init__(self, name,
                 config=BasicRouterConfig,
                 cwd='/tmp',
                 process_manager=ProcessHelper,
                 use_v4=True,
                 use_v6=True,
                 password='zebra',
                 *args, **kwargs):
        """Most of the heavy lifting for this router should happen in the
        associated config object.

        :param config: The configuration generator for this router
        :param cwd: The base directory for temporary files such as configs
        :param process_manager: The class that will manage all the associated
                                processes for this router
        :param use_v4: Wether this router has IPv4
        :param use_v6: Wether this router has IPv6
        :param password: The password for the routing daemons vtysh access"""
        super(Router, self).__init__(name, *args, **kwargs)
        self.use_v4 = use_v4
        self.use_v6 = use_v6
        self.password = password
        self.cwd = cwd
        self._old_sysctl = {}
        self.config = config(self)
        self._processes = process_manager(self)

    def start(self):
        """Start the router: Configure the daemons, set the relevant sysctls,
        and fire up all needed processes"""
        self.cmd('ip', 'link', 'set', 'dev', 'lo', 'up')
        self.config.build()
        for opt, val in self.config.sysctl:
            self._old_sysctl[opt] = self._set_sysctl(opt, val)
        for d in self.config.daemons:
            self._processes.popen(*d.startup_line.split(' '))

    def terminate(self):
        """Stops this router and sets back all sysctls to their old values"""
        self._processes.terminate()
        if not DEBUG_FLAG:
            self.config.cleanup()
        for opt, val in self._old_sysctl.iteritems():
            self._set_sysctl(opt, val)
        super(Router, self).terminate()

    def _set_sysctl(self, key, val):
        """Change a sysctl value, and return the previous set value"""
        val = str(val)
        try:
            v = self._processes.call('sysctl', key)\
                    .split('=')[1]\
                    .strip(' \n\t\r')
        except IndexError:
            v = None
        if v != val:
            self._processes.call('sysctl', '-w', '%s=%s' % (key, val))
        return v