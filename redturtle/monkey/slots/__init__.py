from zope.interface import implements, Interface
from zope.component import getMultiAdapter, adapts

from redturtle.monkey.interfaces import IMailchimpSlot, IMailchimpSlotRenderer


class Slot(object):
    implements(IMailchimpSlot)
    adapts(Interface)
    name = u''

    def __init__(self, context):
        self.context = context

    def render(self, request):
        view = getMultiAdapter((self.context, request), IMailchimpSlotRenderer,
                               name=self.name)
        return view()


class SlotRenderer(object):
    implements(IMailchimpSlotRenderer)
    template = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return self.template()
