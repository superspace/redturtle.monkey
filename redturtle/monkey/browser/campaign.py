from zExceptions import Redirect
from zope.component import getUtility
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView

from redturtle.monkey.interfaces import IMonkeyLocator
from redturtle.monkey.interfaces import ICampaign
#from redturtle.monkey import  _


class CreateCampaign(BrowserView):

    def __call__(self):
        mailchimp = getUtility(IMonkeyLocator)
        subject = self.context.getCampaign_subject()
        list_id = self.context.getCampaign_list()
        template_id = self.context.getCampaign_template()
        title = self.context.title_or_id()
        campaign_id = mailchimp.createCampaign(subject=subject,
                                               list_id=list_id,
                                               title=title,
                                               template_id=template_id)
        if campaign_id:
            IStatusMessage(self.request).add('Mailchimp campaign created: '
              'https://us6.admin.mailchimp.com/campaigns/wizard/confirm?id=%s'
                                                   % campaign_id, type='info')
            raise Redirect, self.request.response.redirect(self.context.absolute_url())

class CanCreateCampaign(BrowserView):
    def __call__(self):
        if ICampaign.providedBy(self.context):
            return True
        else:
            return False
