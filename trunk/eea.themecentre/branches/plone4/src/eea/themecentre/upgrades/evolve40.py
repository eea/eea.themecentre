""" Upgrade scripts for 4.0 version of this package
"""
import transaction
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot

import logging
from Products.ZCatalog.ProgressHandler import ZLogHandler
logger = logging.getLogger("eea.themecentre upgrades 4.0")

def fix_themes_navigation(context):
    """ Add INavigationRoot marker interface for eea.themecentre IThemeTaggable
        objects.
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(
        object_provides='eea.themecentre.interfaces.IThemeCentre')

    logger.info("Fixing eea.themecentre navigation ...")
    pghandler = ZLogHandler(100)
    pghandler.init('Fixing eea.themecentre navigation', len(brains))

    for index, brain in enumerate(brains):
        doc = brain.getObject()
        if not INavigationRoot.providedBy(doc):
            alsoProvides(doc, INavigationRoot)

        pghandler.report(index)
        if index % 100 == 0:
            transaction.savepoint(optimistic=True)

    transaction.savepoint(optimistic=True)
    pghandler.finish()
    logger.info("Fixing eea.themecentre navigation ... DONE")
