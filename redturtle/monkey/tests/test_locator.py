# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.component import getUtility

from redturtle.monkey.testing import \
    REDTURTLE_MONKEY_INTEGRATION_TESTING


class MonkeyLocatorIntegrationTest(unittest.TestCase):

    layer = REDTURTLE_MONKEY_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()

    def test_mailchimp_locator_registration(self):
        from redturtle.monkey.interfaces import IMonkeyLocator
        self.assertTrue(getUtility(IMonkeyLocator))

    def test_mailchimp_locator_connect_method(self):
        from redturtle.monkey.locator import MonkeyLocator
        locator = MonkeyLocator()
        locator.connect()
        self.assertTrue(locator.mailchimp is not False)

    def test_mailchimp_locator_lists_method(self):
        from redturtle.monkey.locator import MonkeyLocator
        locator = MonkeyLocator()
        self.assertTrue(locator.lists())
        self.assertEqual(len(locator.lists()), 2)

    def test_mailchimp_locator_template_method(self):
        from redturtle.monkey.locator import MonkeyLocator
        locator = MonkeyLocator()
        self.assertTrue(locator.templates())
        self.assertEqual(len(locator.templates()), 2)

    def test_mailchimp_locator_create_campaign(self):
        from redturtle.monkey.locator import MonkeyLocator
        locator = MonkeyLocator()
        web_id = locator.createCampaign('Title','Subject','List_id',
                                        'Template_id','The content')
        self.assertEqual(web_id, '123QWE456')

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
