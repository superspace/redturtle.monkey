from zExceptions import Redirect
from zope.component import getUtility
from zope.component import subscribers
from zope.schema.interfaces import IVocabularyFactory
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from plone.uuid.interfaces import IUUID
from plone.app.uuid.utils import uuidToObject

from redturtle.monkey.interfaces import IMonkeyLocator, IMailchimpSlot
from redturtle.monkey import  _


class CampaignWizard(BrowserView):

    def __call__(self):
        """Redirect POST requests to generateCampaign."""
        if self.request.method == 'POST':
            return self.generateCampaign()
        else:
            return super(CampaignWizard, self).__call__()

    def list_templates(self):
        """List all available mailchimp templates."""
        vfactory = getUtility(IVocabularyFactory,
                      name='redturtle.monkey.vocabularies.AvailableTemplates')
        return vfactory(self.context)

    def list_clists(self):
        """List all available mailchimp lists."""
        vfactory = getUtility(IVocabularyFactory,
                      name='redturtle.monkey.vocabularies.AvailableLists')
        return vfactory(self.context)

    def list_slots(self):
        """List all avaible IMailchimpSlot subscribers for given context."""
        vfactory = getUtility(IVocabularyFactory,
                      name='redturtle.monkey.vocabularies.AvailableSlots')
        return vfactory(self.context)

    def list_campaign_items(self):
        """List all campaign items group by folderish/nonfolderish types."""
        items = self.context.getCampaign_items()
        result = []
        for item in items:
            result.append({'uid': IUUID(item),
                           'title': item.title_or_id()})
        return result

    def generateCampaign(self):
        """By calling mailchimp API creates a campaign and redirects
        user to the proper URL."""
        mailchimp = getUtility(IMonkeyLocator)
        form = self.request.form
        subject = form.get('campaign_title')
        list_id = form.get('list')
        template_id = form.get('template')
        title = form.get('campaign_title')

        content = self.generateCampaignContent(form.get('items'))
        if not content:
            IStatusMessage(self.request).add(_(u'Couldn\'t generate campaign items.'))
            raise Redirect,\
                self.request.response.redirect('%s/campaign_wizard' % \
                                                  self.context.absolute_url())

        campaign_id = mailchimp.createCampaign(subject=subject,
                                               list_id=list_id,
                                               title=title,
                                               content=content,
                                               template_id=template_id)
        if campaign_id:
            IStatusMessage(self.request).add(_(u'Mailchimp campaign created.'))
            raise Redirect,\
                self.request.response.redirect('%s/@@campaign_created?id=%s' % \
                            (self.context.absolute_url(), campaign_id))

    def generateCampaignContent(self, items):
        """Tries to render the html content for the campaign items,
        using the slot subscribers."""
        content = {}
        if not items:
            return content

        items_in_slots = {}
        for item in items:
            if not item['enabled']:
                continue
            if item['slot'] not in items_in_slots:
                items_in_slots[item['slot']] = []
            items_in_slots[item['slot']].append(uuidToObject(item['uid']))

        slots = subscribers([self.context], IMailchimpSlot)
        for slot in slots:
            html = slot.render(self.request, items_in_slots.get(slot.name, []))
            if not html: # Let's skip empty slots
                continue
            content['html_%s' % slot.name] = html
        return content
