from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from redturtle.monkey.slots import Slot, SlotRenderer


class Header(Slot):
    name = u'header'


class HeaderRenderer(SlotRenderer):
    template = ViewPageTemplateFile("generic_header.pt")


class Body(Slot):
    name = u'body'


class BodyRenderer(SlotRenderer):
    template = ViewPageTemplateFile("generic_body.pt")
