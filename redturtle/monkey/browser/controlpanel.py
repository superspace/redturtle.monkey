from zope.interface import Invalid
from z3c.form.interfaces import WidgetActionExecutionError
from zope.component import getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.registry.browser import controlpanel

from redturtle.monkey.interfaces import IMonkeySettings
from redturtle.monkey.interfaces import IMonkeyLocator
from redturtle.monkey import _


class MonkeySettingsEditForm(controlpanel.RegistryEditForm):

    schema = IMonkeySettings
    label = _(u"MailChimp settings")
    description = ""

    def updateFields(self):
        super(MonkeySettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(MonkeySettingsEditForm, self).updateWidgets()


class MonkeySettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = MonkeySettingsEditForm
    index = ViewPageTemplateFile('controlpanel.pt')

    def mailchimp_account(self):

        return {}
        # mailchimp = getUtility(IMonkeyLocator)
        # try:
        #     return mailchimp.account()
        # except PostRequestError:
        #     return []
        # except MailChimpError, error:
        #     raise WidgetActionExecutionError(
        #         Invalid(
        #             u"Could not fetch account details from MailChimp. " +
        #             u"Please check your MailChimp API key: %s" % error
        #         )
        #     )
