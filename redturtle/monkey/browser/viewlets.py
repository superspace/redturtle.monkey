# -*- coding: utf-8 -*-
from zope.annotation.interfaces import IAnnotations
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFPlone.i18nl10n import ulocalized_time
from redturtle.monkey.content.campaign import LAST_CAMPAIGN


class LastCampaign(ViewletBase):
    """ This viewlet renders the link to last mailchimp campaign """

    def update(self):
        super(LastCampaign, self).update()
        ann = IAnnotations(self.context)
        self.last_campaign = ann.get(LAST_CAMPAIGN)

    def render(self):
        if self.last_campaign:
            date = self.last_campaign['date']
            if date:
                self.last_campaign['date'] = ulocalized_time(date,
                                                          long_format=True,
                                                          context=self.context)
            return self.index()
        else:
            return ''
