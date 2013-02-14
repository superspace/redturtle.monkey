import unittest2 as unittest

from zope.component import getMultiAdapter
from plone.app.testing import logout, TEST_USER_ID, setRoles
from plone.uuid.interfaces import IUUID

from redturtle.monkey.testing import \
    REDTURTLE_MONKEY_INTEGRATION_TESTING


class TestMonkeyWizard(unittest.TestCase):

    layer = REDTURTLE_MONKEY_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(type_name='Folder', id='f1')
        self.folder = self.portal['f1']
        self.folder.invokeFactory(type_name='Campaign', id='c1')
        self.campaign = self.folder['c1']
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

        # without proper form we should be redirected, too:
        self.assertRaises(Redirect, view.generateCampaign)

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

    def test_monkey_wizard_content_generation(self):
        view = getMultiAdapter((self.campaign, self.request),
                               name="campaign_wizard")

        # First the campaign is empty
        self.assertEqual(view.generateCampaignContent([]), {})

        # Let's add related items
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.folder.invokeFactory(type_name='Event', id='e1')
        self.folder.e1.setTitle(u'Event 1')
        self.folder.invokeFactory(type_name='Event', id='e2')
        self.folder.e2.setTitle(u'Event 2')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        items = [{'slot': 'header',
                  'uid': IUUID(self.folder.e2),
                  'enabled': True},
                 {'slot': 'body',
                  'uid': IUUID(self.folder.e1),
                  'enabled': True}]

        content = view.generateCampaignContent(items)
        self.assertTrue('html_body' in content)
        self.assertTrue('html_header' in content)

        # Finally let's check the HTML
        self.assertTrue('<h1>Event 2</h1>' in content['html_header'])
        self.assertTrue('<h2>Event 1</h2>' in content['html_body'])
