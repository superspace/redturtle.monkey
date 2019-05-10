# from postmonkey import PostMonkey
# from postmonkey import MailChimpException
# from postmonkey.exceptions import PostRequestError

from mailchimp3 import MailChimp

from plone.registry.interfaces import IRegistry
from zope.interface import implements
from zope.component import getUtility

from redturtle.monkey.interfaces import IMonkeyLocator
from redturtle.monkey.interfaces import IMonkeySettings


def connect(func):
    def wrap_connect(self, *args, **kwargs):
        campaign = kwargs.get('campaign')
        if campaign and getattr(campaign,'api_key', False):
            self.settings = campaign
        else:
            registry = getUtility(IRegistry)
            self.settings = registry.forInterface(IMonkeySettings)
        self.mailchimp = MailChimp(self.settings.api_key)
        return func(self, *args, **kwargs)
    return wrap_connect


class MonkeyLocator(object):
    """Utility for MailChimp API calls.
    """
    implements(IMonkeyLocator)

    @connect
    def ping(self, campaign=None):
        """Return simple ping to check if the API is correct"""
        return self.mailchimp.ping.get()

    @connect
    def lists(self, campaign=None):
        """Return all available MailChimp lists.
        http://apidocs.mailchimp.com/api/rtfm/lists.func.php
        """
        #print("MAILCHIMP LOCATOR: lists")
        try:
            # lists returns a dict with 'total' and 'data'. we just need data
            data = self.mailchimp.lists.all(get_all=True, fields="lists.name,lists.id")
            return data['lists']
        except Exception:
            return []
        except Exception:
            return []
        except:
            raise

    @connect
    def templates(self, campaign=None):
        """Return all available MailChimp templates.
        http://apidocs.mailchimp.com/api/rtfm/templates.func.php
        """
        try:
            data = self.mailchimp.templates.all(get_all=True, type="user", fields="templates.id,templates.name")
            return data['templates']
        except Exception:
            return []
        except Exception:
            return []
        except:
            raise

    @connect
    def account(self, campaign=None):
        return {};#self.mailchimp.getAccountDetails()

    @connect
    def createCampaign(self, title, subject, list_id, template_id, content, campaign=None):
        options = {
            'type': 'regular',
            'recipients': {
                'list_id': list_id
            },
            'settings': {
                'subject_line': subject,
                'reply_to': self.settings.from_email,
                'from_name': self.settings.from_name,
                'title': title,
            }
        }
        # try:
        response = self.mailchimp.campaigns.create(options)
        cid = response['id']

        data = {
            'template': {
                'id': int(template_id),
                'sections': content
            }
        }
        self.mailchimp.campaigns.content.update(campaign_id=cid, data=data)

        return cid
        # except Exception:
        #     raise
        # except Exception:
        #     return None
        # except:
        #     raise

    @connect
    def subscribe(self, list_id, email_address, merge_vars, email_type):
        # if not email_type:
        #     email_type = u'html'
        # try:
        #     self.mailchimp.listSubscribe(
        #         id=list_id,
        #         email_address=email_address,
        #         merge_vars=merge_vars,
        #         email_type=email_type,
        #         double_optin=True,
        #         update_existing=False,
        #         replace_interests=True,
        #         send_welcome=False
        #     )
        # except Exception:
        #     raise
        pass