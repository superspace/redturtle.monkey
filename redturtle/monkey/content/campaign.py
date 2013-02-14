"""Definition of the Campaign content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.ATContentTypes.content import schemata
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

from redturtle.monkey import  _
from redturtle.monkey.config import PROJECTNAME
from redturtle.monkey.interfaces import ICampaign


class ImageRadioWidget(atapi.SelectionWidget):
    _properties = atapi.SelectionWidget._properties.copy()
    _properties.update({
        'format': "radio",
        'macro': "imageradio",
        'blurrable': True,
        })


CampaignSchema = ATContentTypeSchema.copy() + atapi.Schema((

#    atapi.StringField('campaign_subject',
#        storage=atapi.AnnotationStorage(),
#        widget=atapi.StringWidget(
#            label=_(u"Subject"),
#            description=_(u"Campaign subject"),
#        ),
#    ),

#    atapi.StringField('campaign_list',
#        storage=atapi.AnnotationStorage(),
#        required=True,
#        vocabulary_factory='redturtle.monkey.vocabularies.AvailableLists',
#        widget=atapi.SelectionWidget(
#            label=_(u"Campaign list"),
#            description=_(u"Choose existing Mailchimp list"),
#        ),
#    ),

    atapi.StringField('campaign_template',
        required=True,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory='redturtle.monkey.vocabularies.AvailableTemplates',
        widget=ImageRadioWidget(
            label=_(u"Campaign template"),
            description=_(u"Choose existing Mailchimp template"),
        ),
    ),

    atapi.ReferenceField('campaign_items',
        relationship = 'campaignItems',
        multiValued = True,
        languageIndependent = False,
        widget = ReferenceBrowserWidget(
            allow_search = True,
            allow_browse = True,
            allow_sorting = True,
            show_indexes = False,
            #base_query= {'portal_type': 'Accessory'},
            force_close_on_insert = True,
            show_results_without_query = True,
            label = _(u'label_campaign_items', default=u'Campaign\'s items'),
            description = '',
            visible = {'edit' : 'visible', 'view' : 'invisible' },
            )
        ),

    ))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

CampaignSchema['title'].storage = atapi.AnnotationStorage()
CampaignSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    CampaignSchema,
    folderish=False,
    moveDiscussion=False
)


class Campaign(ATCTContent):
    """Monkey campaign"""
    implements(ICampaign)

    meta_type = "Campaign"
    schema = CampaignSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(Campaign, PROJECTNAME)
