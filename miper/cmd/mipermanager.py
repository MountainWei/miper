#!/usr/bin/env python
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
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

"""Starter script for Miper Scheduler."""

import eventlet
eventlet.monkey_patch()

import sys

from oslo_config import cfg
from oslo_log import log as logging
from oslo_reports import guru_meditation_report as gmr

from miper import i18n
i18n.enable_lazy()

# Need to register global_opts
from miper.common import config  # noqa
from miper import objects
from miper import service
from miper import utils
from miper import version


CONF = cfg.CONF


def main():
    objects.register_all()
    CONF(sys.argv[1:], project='miper',
         version=version.version_string())
    logging.setup(CONF, "miper")
    utils.monkey_patch()
    gmr.TextGuruMeditation.setup_autorun(version)
    server = service.Service.create(binary='miper-mipermanager')
    service.serve(server)
    service.wait()
