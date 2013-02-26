from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from redturtle.monkey.slots import Slot, SlotRenderer


class Header(Slot):
    name = u'main_primopiano'

class HeaderRenderer(SlotRenderer):
    template = ViewPageTemplateFile("main-primopiano.pt")


class Body(Slot):
    name = u'main_other'

class BodyRenderer(SlotRenderer):
    template = ViewPageTemplateFile("main-other.pt")


class PreHeaderContent(Slot):
    name = u'preheader_content'
    template = ViewPageTemplateFile("preheader_content.pt")

    def render(self, objs=None, title=None,
               description=None, number=None):
        return self.template(description=description)


class CampaignTitle(Slot):
    name = u'campaign_title'
    template = ViewPageTemplateFile("campaign-title.pt")

    def render(self, objs=None, title=None,
               description=None, number=None):
        return self.template(title=title)


class HeaderNumber(Slot):
    name = u'header_number'
    template = ViewPageTemplateFile("header-number.pt")

    def render(self, objs=None, title=None,
               description=None, number=None):
        return self.template(number=number)


class HeaderTitle(Slot):
    name = u'header_title'
    template = ViewPageTemplateFile("header-title.pt")

    def render(self, objs=None, title=None,
               description=None, number=None):
        return self.template(title=title)
