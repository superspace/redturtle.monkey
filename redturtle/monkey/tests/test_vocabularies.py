import unittest2 as unittest
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from redturtle.monkey.testing import \
    REDTURTLE_MONKEY_INTEGRATION_TESTING


class TestMonkeyVocabularies(unittest.TestCase):

    layer = REDTURTLE_MONKEY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_template_vocabs(self):
        vfactory = getUtility(IVocabularyFactory,
                      name='redturtle.monkey.vocabularies.AvailableTemplates')
        vocab = vfactory(self.portal)
        self.assertTrue(u'<img src="http://nohost/preview.jpg" title="My template"/>' in \
                                                     [a.title for a in vocab])
