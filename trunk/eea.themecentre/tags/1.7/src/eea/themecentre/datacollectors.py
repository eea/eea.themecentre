from Products.ThemeCentre.mergedtheme import getFeedsForSynonymousThemes

from eea.rdfrepository.interfaces import IRDFPortletDataCollector
from eea.themecentre.interfaces import IThemeCentre
from eea.themecentre.themecentre import getTheme
from zope.component import adapts
from zope.interface import implements

class RDFPortletDataCollector(object):
    implements(IRDFPortletDataCollector)
    adapts(IThemeCentre)

    def __init__(self, context):
        self.context = context

    @property
    def feeds(self):
        currentTheme = getTheme(self.context)
        if currentTheme:
            return getFeedsForSynonymousThemes(currentTheme)
