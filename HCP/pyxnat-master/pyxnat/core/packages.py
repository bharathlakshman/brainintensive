# package.py
# pyxnat support for ConnectomeDB download packages
# 
# Copyright (c) 2013 Washington University School of Medicine
# Author: Kevin A. Archie <karchie@wustl.edu>

import json, os, platform, subprocess
from itertools import chain
from pyxnat import __version__
from .resources import EObject

def _join(xs, separator=','):
    """If xs is a string, return it;
    Otherwise, treat it as an iterable. If the first element is
    a pyxnat EObject, call label() on each element and join the
    result with separators. If not an EObject, join the elements
    directly (hoping that they're strings).
    """
    if isinstance(xs,basestring):
        return xs;
    try:
        xsi = iter(xs)
        first = xsi.next()
    except StopIteration:
        return None
    else:
        xsi = chain([first],xsi)
        if isinstance(first,EObject):
            return separator.join([x.label() for x in xsi])
        else:
            return separator.join(xsi)

_system = platform.system();
_connectpaths = { 'Darwin': '/Applications/Aspera Connect.app',
                 'Linux': '/.aspera/connect' }
_connectpath = _connectpaths[_system]
_binpaths = { 'Darwin': '/Contents/Resources', 'Linux': '/bin' }
_binpath = _binpaths[_system]
_etcpaths = { 'Darwin': '/Contents/Resources', 'Linux': '/etc' }
_etcpath = _etcpaths[_system]

def _aspera_connectdir():
    return os.getenv('ASPERA_CONNECTDIR') or \
        os.getenv('HOME') + _connectpath

def _aspera_bindir():
    return os.getenv('ASPERA_BINDIR') or _aspera_connectdir() + _binpath

def _aspera_etcdir():
    return os.getenv('ASPERA_ETCDIR') or _aspera_connectdir() + _etcpath

def _aspera_ascp():
    return os.getenv('ASCP') or _aspera_bindir() + '/ascp'

_xfer_spec_mapping = {
    'remote_user': '--user',
    'min_rate_kbps': '-m',
    'target_rate_kbps': '-l',
    'fasp_port': '-O',
    'ssh_port': '-P',
    'remote_host': '--host',
    'rate_policy': '--policy',
    'token': '-W'
    }

class Packages(object):
    """Download packages"""

    def __init__(self, interface):
        """
        Parameters
        ----------
        interface: :class:`Interface`
          Main interface reference
        """
        self._intf = interface

    def __iter__(self):
        """ Enumerates the package types. """
        return (p['id'] for p in json.loads(self._intf._exec('/spring/download'))['packages'])

    def list(self):
        """ Enumerates the package types. """
        return list(self)

    def _request(self, subjects, packages, add_query_params):
        subjects = _join(subjects)
        packages = _join(packages)
        qps = ['subjects=' + subjects]
        if packages:
            qps.append('package=' + packages)
        qps.extend(add_query_params)
        return '/spring/download?' + _join(qps, separator='&')

    def _do_request(self, subjects, packages, add_query_params,
                    method='POST'):
        request = self._request(subjects, packages, add_query_params)
        return json.loads(self._intf._exec(request, method=method))
        
    def _get_xfer_spec(self, subjects, packages, dest=None):
        """ Get an Aspera transfer_spec to download the named
        packages for the named subjects. subjects and packages
        may be a string or an iterable of strings. If destination
        is provided, puts files in that directory; otherwise,
        files are put in working directory."""
        return self._do_request(subjects, packages, 
                                ['destination='+dest] if dest else [])

    def _apply_xfer_spec(self, xfer_spec):
        """ Uses ascp to perform the download described in xfer_spec."""
        command = [_aspera_ascp(), '-p']
        command.append('-i')
        command.append(_aspera_etcdir() + '/asperaweb_id_dsa.openssh')
        for key, val in xfer_spec.iteritems():
            if key in _xfer_spec_mapping:
                arg = _xfer_spec_mapping[key]
                if arg.startswith('--'):
                    command.append(arg + '=' + val)
                else:
                    command.append(arg)
                    command.append(str(val))

        if 'direction' in xfer_spec and "receive" != xfer_spec['direction']:
            raise Exception('only ascp receives are supported')
        command.append("--mode=recv")

        for pathm in xfer_spec['paths']:
            command.append(pathm['source'])

        command.append('destination_root' in xfer_spec
                       and xfer_spec['destination_root']
                       or '.')
        subprocess.check_output(command, env = {
            'ASPERA_SCP_COOKIE' :
            'XDATUser={};User-Agent=pyxnat {}/{} {}'.format(
                self._intf._user, __version__,
                platform.python_implementation(), platform.python_version())
        })

    def download(self, subjects, packages, dest=None):
        """ Use the Aspera command-line client to download the named
        packages for the named subjects. subjects and packages may be
        a string or an iterable of strings. If destination is
        provided, puts files in that directory; otherwise, files are
        put in working directory."""
        xfer_spec = self._get_xfer_spec(subjects, packages, dest)
        self._apply_xfer_spec(xfer_spec)

    def for_subjects(self, subjects, packages=[]):
        """ Get package availability information for the named
        subjects; if package names are provided, get file count and
        size for those packages only."""
        return self._do_request(subjects, packages,
                                ['view=subjects' if packages else 'view=packages'])
