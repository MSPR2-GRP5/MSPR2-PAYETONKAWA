from django.test import TestCase

from django.test import TestCase


class MockTestCase(TestCase):

    def test_mock_test(self):
        self.assertEqual(True, True)
        print("Mock testcase successfully run")
