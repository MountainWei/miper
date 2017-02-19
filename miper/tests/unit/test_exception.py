
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

from miper import exception
from miper import test

import six


class FakeNotifier(object):
    """Acts like the miper.openstack.common.notifier.api module."""
    ERROR = 88

    def __init__(self):
        self.provided_publisher = None
        self.provided_event = None
        self.provided_priority = None
        self.provided_payload = None

    def notify(self, context, publisher, event, priority, payload):
        self.provided_publisher = publisher
        self.provided_event = event
        self.provided_priority = priority
        self.provided_payload = payload


def good_function():
    return 99


def bad_function_error():
    raise exception.Error()


def bad_function_exception():
    raise test.TestingException()


class MiperExceptionTestCase(test.TestCase):
    def test_default_error_msg(self):
        class FakeMiperException(exception.MiperException):
            message = "default message"

        exc = FakeMiperException()
        self.assertEqual('default message', six.text_type(exc))

    def test_error_msg(self):
        self.assertEqual('test',
                         six.text_type(exception.MiperException('test')))

    def test_default_error_msg_with_kwargs(self):
        class FakeMiperException(exception.MiperException):
            message = "default message: %(code)s"

        exc = FakeMiperException(code=500)
        self.assertEqual('default message: 500', six.text_type(exc))

    def test_error_msg_exception_with_kwargs(self):
        # NOTE(dprince): disable format errors for this test
        self.flags(fatal_exception_format_errors=False)

        class FakeMiperException(exception.MiperException):
            message = "default message: %(misspelled_code)s"

        exc = FakeMiperException(code=500)
        self.assertEqual('default message: %(misspelled_code)s',
                         six.text_type(exc))

    def test_default_error_code(self):
        class FakeMiperException(exception.MiperException):
            code = 404

        exc = FakeMiperException()
        self.assertEqual(404, exc.kwargs['code'])

    def test_error_code_from_kwarg(self):
        class FakeMiperException(exception.MiperException):
            code = 500

        exc = FakeMiperException(code=404)
        self.assertEqual(404, exc.kwargs['code'])

    def test_error_msg_is_exception_to_string(self):
        msg = 'test message'
        exc1 = Exception(msg)
        exc2 = exception.MiperException(exc1)
        self.assertEqual(msg, exc2.msg)

    def test_exception_kwargs_to_string(self):
        msg = 'test message'
        exc1 = Exception(msg)
        exc2 = exception.MiperException(kwarg1=exc1)
        self.assertEqual(msg, exc2.kwargs['kwarg1'])

    def test_message_in_format_string(self):
        class FakeMiperException(exception.MiperException):
            message = 'FakeMiperException: %(message)s'

        exc = FakeMiperException(message='message')
        self.assertEqual('FakeMiperException: message', six.text_type(exc))

    def test_message_and_kwarg_in_format_string(self):
        class FakeMiperException(exception.MiperException):
            message = 'Error %(code)d: %(message)s'

        exc = FakeMiperException(message='message', code=404)
        self.assertEqual('Error 404: message', six.text_type(exc))

    def test_message_is_exception_in_format_string(self):
        class FakeMiperException(exception.MiperException):
            message = 'Exception: %(message)s'

        msg = 'test message'
        exc1 = Exception(msg)
        exc2 = FakeMiperException(message=exc1)
        self.assertEqual('Exception: test message', six.text_type(exc2))
