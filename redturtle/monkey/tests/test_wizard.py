import unittest2 as unittest

from zope.component import getMultiAdapter
from plone.app.testing import logout, TEST_USER_ID, setRoles

from redturtle.monkey.testing import \
    REDTURTLE_MONKEY_INTEGRATION_TESTING


class TestMonkeyWizard(unittest.TestCase):

    layer = REDTURTLE_MONKEY_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(type_name='Campaign', id='c1')
        self.campaign = self.portal['c1']
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def test_monkey_wizard_view_vocabularies(self):
        view = getMultiAdapter((self.campaign, self.request),
                               name="campaign_wizard")
        self.assertTrue('ACME Newsletter' in [a.title
                                              for a in view.list_clists()])
        self.assertTrue('My template' in [a.title
                                          for a in view.list_templates()])

    def test_monkey_wizard_generate_campaign(self):
        from zExceptions import Redirect

        view = getMultiAdapter((self.campaign, self.request),
                               name="campaign_wizard")

        # without proper form we should get KeyErrors:
        self.assertRaises(KeyError, view.generateCampaign)

        self.request.form['campaign_title'] = 'Title'
        self.request.form['list'] = 'List id'
        self.request.form['template'] = 'Template id'

        # now we should get a proper Redirect
        self.assertRaises(Redirect, view.generateCampaign)

    def test_monkey_wizard_view_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(
            Unauthorized,
            self.campaign.restrictedTraverse,
            '@@campaign_wizard'
        )
