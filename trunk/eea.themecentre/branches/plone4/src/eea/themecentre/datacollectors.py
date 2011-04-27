""" Data collectors module
"""
#TODO: fix me
#from Products.ThemeCentre.mergedtheme import getFeedsForSynonymousThemes
#TODO: fix me
#from eea.rdfrepository.interfaces import IRDFPortletDataCollector
from eea.themecentre.interfaces import IThemeCentre
from eea.themecentre.themecentre import getTheme
from zope.component import adapts
from zope.interface import implements

#TODO: fix me
# - just delete the dummy interface
from zope.interface import Interface
class IRDFPortletDataCollector(Interface):
    """ Dummy interface
    """

class RDFPortletDataCollector(object):
    implements(IRDFPortletDataCollector)
    adapts(IThemeCentre)

    def __init__(self, context):
        self.context = context

    @property
    def feeds(self):
        currentTheme = getTheme(self.context)
        if currentTheme:
            #TODO: fix me
            #return getFeedsForSynonymousThemes(currentTheme)
            return []
