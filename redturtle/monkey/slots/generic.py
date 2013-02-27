from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from redturtle.monkey.slots import Slot, SlotRenderer


class Header(Slot):
    name = u'main_primopiano'

class HeaderRenderer(SlotRenderer):
    template = ViewPageTemplateFile("main-primopiano.pt")


class Body(Slot):
    name = u'main_body'

class BodyRenderer(SlotRenderer):
    template = ViewPageTemplateFile("main-body.pt")


class PreHeaderContent(Slot):
    name = u'preheader_content'
    template = ViewPageTemplateFile("preheader_content.pt")

    def render(self, objs=None, **kw):
        if kw.get('description'):
            return self.template(description=kw['description'])


class CampaignTitle(Slot):
    name = u'campaign_title'
    template = ViewPageTemplateFile("campaign-title.pt")

    def render(self, objs=None, **kw):
        if kw.get('title'):
            return self.template(title=kw['title'])


class HeaderNumber(Slot):
    name = u'header_number'
    template = ViewPageTemplateFile("header-number.pt")

    def render(self, objs=None, **kw):
        if kw.get('number'):
            return self.template(number=kw['number'])


class HeaderTitle(Slot):
    name = u'header_title'
    template = ViewPageTemplateFile("header-title.pt")

    def render(self, objs=None, **kw):
        if kw.get('description'):
            return self.template(title=kw['description'])
