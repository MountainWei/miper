# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright 2012 Red Hat, Inc.
# Copyright 2013 NTT corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Command-line flag library.

Emulates gflags by wrapping cfg.ConfigOpts.

The idea is to move fully to cfg eventually, and this wrapper is a
stepping stone.

"""

import socket

from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import netutils

from miper.i18n import _


CONF = cfg.CONF
logging.register_options(CONF)

core_opts = [
    cfg.StrOpt('api_paste_config',
               default="api-paste.ini",
               help='File name for the paste.deploy config for miper-api'),
    cfg.StrOpt('state_path',
               default='/var/lib/miper',
               deprecated_name='pybasedir',
               help="Top-level directory for maintaining miper's state"), ]

debug_opts = [
]

CONF.register_cli_opts(core_opts)
CONF.register_cli_opts(debug_opts)

global_opts = [
    cfg.StrOpt('my_ip',
               default=netutils.get_my_ipv4(),
               help='IP address of this host'),
    cfg.StrOpt('mipermanager_topic',
               default='miper-mipermanager',
               help='The topic that mipermanager nodes listen on'),
    cfg.BoolOpt('enable_v1_api',
                default=True,
                help=_("DEPRECATED: Deploy v1 of the Miper API.")),
    cfg.BoolOpt('api_rate_limit',
                default=True,
                help='Enables or disables rate limit of the API.'),
    cfg.ListOpt('osapi_miper_ext_list',
                default=[],
                help='Specify list of extensions to load when using osapi_'
                     'miper_extension option with miper.api.contrib.'
                     'select_extensions'),
    cfg.MultiStrOpt('osapi_miper_extension',
                    default=['miper.api.contrib.standard_extensions'],
                    help='osapi miper extension to load'),
    cfg.StrOpt('mipermanager_manager',
               default='miper.mipermanager.manager.MipermanagerManager',
               help='Full class name for the Manager for mipermanager'),
    cfg.StrOpt('host',
               default=socket.gethostname(),
               help='Name of this node.  This can be an opaque identifier. '
                    'It is not necessarily a host name, FQDN, or IP address.'),
    cfg.StrOpt('rootwrap_config',
               default='/etc/miper/rootwrap.conf',
               help='Path to the rootwrap configuration file to use for '
                    'running commands as root'),
    cfg.BoolOpt('monkey_patch',
                default=False,
                help='Enable monkey patching'),
    cfg.ListOpt('monkey_patch_modules',
                default=[],
                help='List of modules/decorators to monkey patch'),
    cfg.StrOpt('mipermanager_api_class',
               default='miper.mipermanager.api.API',
               help='The full class name of the mipermanager API class to use'),
    cfg.StrOpt('auth_strategy',
               default='keystone',
               choices=['noauth', 'keystone', 'deprecated'],
               help='The strategy to use for auth. Supports noauth, keystone, '
                    'and deprecated.'),
    cfg.StrOpt('os_privileged_user_name',
               default=None,
               help='OpenStack privileged account username. Used for requests '
                    'to other services (such as Nova) that require an account '
                    'with special rights.'),
    cfg.StrOpt('os_privileged_user_password',
               default=None,
               help='Password associated with the OpenStack privileged '
                    'account.',
               secret=True),
    cfg.StrOpt('os_privileged_user_tenant',
               default=None,
               help='Tenant name associated with the OpenStack privileged '
                    'account.'),
    cfg.StrOpt('os_privileged_user_auth_url',
               default=None,
               help='Auth URL associated with the OpenStack privileged '
                    'account.'),
]

CONF.register_opts(global_opts)
