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

    def ping(self):
        """Return simple ping to check if the API is correct"""
        self.connect()
        return self.mailchimp.ping()

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

    def createCampaign(self, title, subject, list_id, template_id, content):
        self.connect()
        options = {'subject': subject,
                   'list_id': list_id,
                   'template_id': template_id,
                   'title': title,
                   'from_email': self.settings.from_email,
                   'from_name': self.settings.from_name}
        try:
            cid = self.mailchimp.campaignCreate(type='regular', options=options, content=content)
            campaign = self.mailchimp.campaigns(filters={'campaign_id':cid})
            return campaign['data'][0]['web_id']
        except MailChimpException:
            return None
        except PostRequestError:
            return None
        except:
            raise
