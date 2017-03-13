""" Catalog module
"""
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface
from eea.themecentre.interfaces import IThemeTagging
from plone.indexer.decorator import indexer
try:
    from eea.mediacentre import interfaces
    IMediaType = interfaces.IMediaType
except (ImportError, AttributeError):
    class IMediaType(Interface):
        """ IMediaType """

@indexer(Interface)
def getThemesForIndex(obj, **kwargs):
    """ Get themes for catalog index """
    try:
        themes = IThemeTagging(obj)
        return themes.tags
    except (ComponentLookupError, TypeError, ValueError):
        # if can't be adapted, see if it's an AT object with getThemes method
        if hasattr(obj, 'getThemes'):
            return obj.getThemes()

        # The catalog expects AttributeErrors when a value can't be found
        raise AttributeError

@indexer(Interface)
def getMediaTypes(obj, **kwargs):
    """ Get media types """
    try:
        adapter = IMediaType(obj)
        return adapter.types
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError
