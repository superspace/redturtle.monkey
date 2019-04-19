from plone import api
from Products.CMFCore.utils import getToolByName
import logging

PROFILE_ID = 'profile-redturtle.monkey:default'

def step_1000_to_1100(context, logger=None):
    if logger is None:
        logger = logging.getLogger('redturtle.monkey')
   
    portal = api.portal.get()
    setup = getToolByName(portal, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')

