import random
from zExceptions import Redirect
from zope.component import getUtility
from zope.component import subscribers
from zope.schema.interfaces import IVocabularyFactory
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView

from redturtle.monkey.interfaces import IMonkeyLocator, IMailchimpSlot
from redturtle.monkey import  _


class CampaignWizard(BrowserView):

    def list_templates(self):
        vfactory = getUtility(IVocabularyFactory,
                      name='redturtle.monkey.vocabularies.AvailableTemplates')
        return vfactory(self.context)

    def list_clists(self):
        vfactory = getUtility(IVocabularyFactory,
                      name='redturtle.monkey.vocabularies.AvailableLists')
        return vfactory(self.context)

    def __call__(self):
        if self.request.method == 'POST':
            return self.generateCampaign()
        else:
            return super(CampaignWizard, self).__call__()

    def generateCampaign(self):
        mailchimp = getUtility(IMonkeyLocator)
        form = self.request.form
        subject = form['campaign_title']
        list_id = form['list']
        template_id = form['template']
        title = form['campaign_title']
        content = self.generateCampaignContent()
        campaign_id = mailchimp.createCampaign(subject=subject,
                                               list_id=list_id,
                                               title=title,
                                               content=content,
                                               template_id=template_id)
        if campaign_id:
            IStatusMessage(self.request).add(_(u'Mailchimp campaign created.'))
            raise Redirect, self.request.response.redirect('%s/@@campaign_created?id=%s' % \
                                   (self.context.absolute_url(), campaign_id))

    def generateCampaignContent(self):
        content = {}
        for item in self.context.getCampaign_items():
            slots = subscribers([item], IMailchimpSlot)
            for slot in slots:
                slot_name = 'html_%s' % slot.name
                if slot_name not in content:
                    content[slot_name] = ''
                content[slot_name] += slot.render(self.request)
        return content

    def old_generateCampaignContent(self):
        content = {'html_std_content01':'',
                   'html_std_content02':'',
                   'html_std_content00':''}
        template = "<h3>%s</h3><p>%s</p><a href='%s'>Read more...</a>"
        sections = content.keys()
        for item in self.context.getCampaign_items():
            section = random.choice(sections)
            content[section] += template % (item.title_or_id(), item.Description(), item.absolute_url())
        return content
