from zope.component import getUtility
from zope.component import subscribers
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from redturtle.monkey.interfaces import IMonkeyLocator, IMailchimpSlot


def available_lists(context):
    mailchimp = getUtility(IMonkeyLocator)
    lists = mailchimp.lists()
    if not lists:
        return SimpleVocabulary([])
    return SimpleVocabulary([
        SimpleTerm(value=li['id'], title=li['name']) for li in lists]
    )


def available_templates(context):
    mailchimp = getUtility(IMonkeyLocator)
    templates = mailchimp.templates()
    if not templates:
        return SimpleVocabulary([])
    return SimpleVocabulary([
        SimpleTerm(value=str(li['id']), title=li['name']) for li in templates]
    )


def available_slots(context):
    slots = subscribers([context], IMailchimpSlot)
    return SimpleVocabulary([
        SimpleTerm(value=str(li.name), title=li.name) for li in slots]
    )
