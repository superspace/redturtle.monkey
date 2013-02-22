from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from redturtle.monkey.slots import SlotRenderer


class BodyRenderer(SlotRenderer):
    template = ViewPageTemplateFile("event_body.pt")
