from oslo_versionedobjects.tests import test_objects

from miper import objects


class BaseObjectsTestCase(test_objects._LocalTest):
    def setUp(self):
        super(BaseObjectsTestCase, self).setUp()
        # Import miper objects for test cases
        objects.register_all()
