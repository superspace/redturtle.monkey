import random
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
        content = self.generateCampaignContent()
        campaign_id = mailchimp.createCampaign(subject=subject,
                                               list_id=list_id,
                                               title=title,
                                               content=content,
                                               template_id=template_id)
        if campaign_id:
            IStatusMessage(self.request).add('Mailchimp campaign created.')
            raise Redirect, self.request.response.redirect('%s/@@campaign_created?id=%s' % \
                                   (self.context.absolute_url(), campaign_id))

    def generateCampaignContent(self):
        content = {'html_std_content01':'',
                   'html_std_content02':'',
                   'html_std_content00':''}
        template = "<h3>%s</h3><p>%s</p><a href='%s'>Read more...</a>"
        sections = content.keys()
        for item in self.context.getCampaign_items():
            section = random.choice(sections)
            content[section] += template % (item.title_or_id(), item.Description(), item.absolute_url())
        return content

class CanCreateCampaign(BrowserView):
    def __call__(self):
        if ICampaign.providedBy(self.context):
            return True
        else:
            return False
