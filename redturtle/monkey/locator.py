from postmonkey import PostMonkey
from postmonkey import MailChimpException
from postmonkey.exceptions import PostRequestError
from plone.registry.interfaces import IRegistry
from zope.interface import implements
from zope.component import getUtility

from redturtle.monkey.interfaces import IMonkeyLocator
from redturtle.monkey.interfaces import IMonkeySettings


class MonkeyLocator(object):
    """Utility for MailChimp API calls.
    """

    implements(IMonkeyLocator)

    def connect(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IMonkeySettings)
        self.mailchimp = PostMonkey(self.settings.api_key)

    def lists(self):
        """Return all available MailChimp lists.
        http://apidocs.mailchimp.com/api/rtfm/lists.func.php
        """
        #print("MAILCHIMP LOCATOR: lists")
        self.connect()
        try:
            # lists returns a dict with 'total' and 'data'. we just need data
            return self.mailchimp.lists()['data']
        except MailChimpException:
            return []
        except PostRequestError:
            return []
        except:
            raise

    def templates(self):
        """Return all available MailChimp templates.
        http://apidocs.mailchimp.com/api/rtfm/templates.func.php
        """
        self.connect()
        try:
            return self.mailchimp.templates()['user']
        except MailChimpException:
            return []
        except PostRequestError:
            return []
        except:
            raise

    def account(self):
        self.connect()
        return self.mailchimp.getAccountDetails()
