from Acquisition import aq_inner
from zope.interface import alsoProvides
from z3c.form.interfaces import IFormLayer
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform import z2
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import implements
from zope import schema

from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from z3cformhelpers import AddForm
from z3cformhelpers import EditForm

from redturtle.monkey import  _
from redturtle.monkey.interfaces import INewsletterSubscribe
from redturtle.monkey.browser.newsletter import NewsletterSubscriberForm


class IMailChimpPortlet(IPortletDataProvider):

    name = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of the portlet'))

    list_id = schema.Choice(
        title=_(u'Available lists'),
        description=_(u'Select list to subscribe to.'),
        required=True,
        vocabulary='redturtle.monkey.vocabularies.AvailableLists'
        )


class Assignment(base.Assignment):
    implements(IMailChimpPortlet)

    def __init__(self, name=u'', list_id=u''):
        self.name = name
        self.list_id = list_id

    @property
    def title(self):
        return _(u"MailChimp")


class Renderer(base.Renderer):
    fields = field.Fields(INewsletterSubscribe)
    _template = ViewPageTemplateFile('subscribe.pt')
    form = NewsletterSubscriberForm

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

# XXX: This breaks the test_edit_portlet test because the entire portlet is
# cached in the test and changes will not show up.
#    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def name(self):
        return self.data.name or _(u"Subscribe to newsletter")

    def update(self):
        super(Renderer, self).update()
        z2.switch_on(self, request_layer=IFormLayer)
        self.form = self.form(aq_inner(self.context), self.request)
        self.form.portlet = self.data
        alsoProvides(self.form, IWrappedForm)
        self.form.update()


class AddForm(AddForm):
    fields = field.Fields(IMailChimpPortlet)
    label = _(u"Add MailChimp Portlet")
    description = _(
        u"This portlet displays a subscription form for a " +
        u"MailChimp newsletter.")

    def create(self, data):
        return Assignment(
            name=data.get('name', u''),
            list_id=data.get('list_id', u''))


class EditForm(EditForm):
    fields = field.Fields(IMailChimpPortlet)
    label = _(u"Edit MailChimp Portlet")
    description = _(
        u"This portlet displays a subscription form for a " +
        u"MailChimp newsletter.")
