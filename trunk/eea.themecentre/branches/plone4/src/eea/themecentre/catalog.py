""" Catalog module
"""
#TODO: fix me plone4
#from zope.component.exceptions import ComponentLookupError
from zope.interface import providedBy, Interface
from eea.themecentre.interfaces import IThemeTagging
#TODO: fix me plone4
#from eea.mediacentre.interfaces import IMediaType
from Products.CMFCore.utils import getToolByName
from plone.indexer.decorator import indexer

#TODO: not used? plone4
def getSynonyms(portal):
    # used to return true synonyms
    vocabularies = getToolByName(portal, 'portal_vocabularies')
    root = getattr(vocabularies, 'themesmerged', None)
    synonyms = {}

    for secondLevel in root.objectValues():
        synonymous_themes = secondLevel.objectIds()
        for index, theme in enumerate(synonymous_themes):
            synonyms[theme] = synonymous_themes[:index] + synonymous_themes[index+1:]

    return synonyms

@indexer(Interface)
def getThemesForIndex(obj, **kwargs):
    try:
        themes = IThemeTagging(obj)
        return themes.tags
    #TODO: fix me plone4
    #except (ComponentLookupError, TypeError, ValueError):
    except (TypeError, ValueError):
        # if can't be adapted, see if it's an AT object with getThemes method
        if hasattr(obj, 'getThemes'):
            return obj.getThemes()

        # The catalog expects AttributeErrors when a value can't be found
        raise AttributeError

@indexer(Interface)
def getMediaTypes(obj, **kwargs):
    try:
        #TODO: fix me plone4
        #adapter = IMediaType(obj)
        #return adapter.types
        return ''
    #TODO: fix me plone4
    #except (ComponentLookupError, TypeError, ValueError):
    except (TypeError, ValueError):
        raise AttributeError
