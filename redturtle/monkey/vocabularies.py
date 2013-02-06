from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from redturtle.monkey.interfaces import IMonkeyLocator


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
