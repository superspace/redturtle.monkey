# XXX from postmonkey import PostMonkey
# XXX from postmonkey import MailChimpException
# XXX from postmonkey.exceptions import PostRequestError
from plone.registry.interfaces import IRegistry
from zope.interface import implements
from zope.component import getUtility

from redturtle.monkey.interfaces import IMonkeyLocator
from redturtle.monkey.interfaces import IMonkeySettings

from mailchimp3 import MailChimp
from mailchimp3 import helpers


def connect(func):
    def wrap_connect(self, *args, **kwargs):
        campaign = kwargs.get('campaign')
        if campaign and getattr(campaign,'api_key', False):
            self.settings = campaign
        else:
            registry = getUtility(IRegistry)
            self.settings = registry.forInterface(IMonkeySettings)
        self.mailchimp = MailChimp(mc_api=self.settings.api_key)
        return func(self, *args, **kwargs)
    return wrap_connect


class MonkeyLocator(object):
    """Utility for MailChimp API calls.
    """
    implements(IMonkeyLocator)

    @connect
    def ping(self, campaign=None):
        """Return simple ping to check if the API is correct"""
        KEYWORD = u'health_status'
        STATUS = u"Everything's Chimpy!"
        status = self.mailchimp.ping.get()
        return KEYWORD in status and status[KEYWORD] == STATUS

    @connect
    def lists(self, campaign=None):
        """Return all available MailChimp lists.
        http://apidocs.mailchimp.com/api/rtfm/lists.func.php
        """
        #print("MAILCHIMP LOCATOR: lists")
        try:
            # lists returns a dict with 'total' and 'data'. we just need data
            return self.mailchimp.lists.all()['lists']
        # XXX except MailChimpException:
        # except Exception, e:
        #     return []
        # # XXX except PostRequestError:
        #     return []
        except:
            raise

    @connect
    def templates(self, campaign=None):
        """Return all available MailChimp templates.
        http://apidocs.mailchimp.com/api/rtfm/templates.func.php
        """
        try:
            # XXX OCCHIO CHE QUESTA E' PER FTA: SERVE FARE UN QUALCOSA NEL REGISTRY PER
            # SALVARSELO. ANCHE SENZA INTERFACCIA FIGA. SOLO UNA ENTRY NEL REGISTRY.
            #folder_id='75977c3d27'
            folder_id = self.settings.folder_id
            return self.mailchimp.templates.all(folder_id=folder_id)['templates']
        # # XXX except MailChimpException:
        # except Exception:
        #     return []
        # # XXX except PostRequestError:
        # except Exception:
        #     return []
        except:
            raise

    @connect
    def account(self, campaign=None):
        return self.mailchimp.getAccountDetails()

    @connect
    def createCampaign(self, title, subject, list_id, template_id, content, campaign=None):
        # options = {'subject': subject,  #
        #            'list_id': list_id,  #
        #            'template_id': template_id, #
        #            'title': title, #
        #            'from_email': self.settings.from_email, ##
        #            'from_name': self.settings.from_name} ##
        try:
            payload = {
                "recipients": {
                        "list_id": list_id,
                },
                "settings": {
                        "subject_line": subject,
                        "from_name": self.settings.from_name,
                        "reply_to": self.settings.from_email,
                        "template_id": int(template_id),
                        "title": title,
                },
                "type": "regular",
            }
            # cid = self.mailchimp.campaigns(type='regular', options=options, content=content)
            cid = self.mailchimp.campaigns.create(payload)
            # self.mailchimp.campaigns.set_content(campaign_id=cid['id'], data=content)
            content2 = {}
            # XXX change the way these data are charged on dict
            for key in content:
                content2[key.replace('html_', '')] = content[key]
            content.update(content2)

            update_payload = {
                "template": {
                    "id": int(template_id),
                    "sections": content
                }
            }
            self.mailchimp.campaigns.content.update(campaign_id=cid['id'], data=update_payload)
            # XXX campaign = self.mailchimp.campaigns(filters={'campaign_id':cid}) sembra non servire
            # XXX return campaign['data'][0]['web_id']
            return cid[u'web_id']
        # # except MailChimpException:
        # except Exception:
        #     raise
        # # except PostRequestError:
        # except Exception:
        #     return None
        except:
            raise

    @connect
    def get_user_data_subscription(self, email, list_id):
        helpers.check_email(email)
        #md5_email = helpers.get_subscriber_hash(email)
        #info_url = '/3.0/lists/%s/members/%s' % (list_id, md5_email)
        #result = self.mailchimp.lists._mc_client._get(url=info_url)
        
        data = {"members": 
                [{"email_address": email, "status": "pending"}],
                "update_existing": True
               }

        return data

    @connect
    def subscribe(self, list_id, email_address, merge_vars, email_type):
        if not email_type:
            email_type = u'html'
        data = self.get_user_data_subscription(email_address, list_id)
        try:
            self.mailchimp.lists.update_members(list_id, data)
        # XXX except MailChimpException:
        except Exception:
            raise
