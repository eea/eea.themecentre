from Products.ATContentTypes.content.event import ATEvent
from Products.ATContentTypes.content.image import ATImage
from Products.CMFCore.utils import getToolByName
from Products.EEAContentTypes.content.Highlight import Highlight
from Products.EEAContentTypes.content.PressRelease import PressRelease

from eea.themecentre.interfaces import IThemeMoreLink
from eea.themecentre.themecentre import getThemeCentreByName
from p4a.video.interfaces import IVideoEnhanced
from zope.component import adapts
from zope.interface import Interface, implements

class LinkAdapter(object):
    adapts(Interface)
    implements(IThemeMoreLink)

    def __init__(self, context):
        self.context = context

    def _themecentre(self, theme):
        return getThemeCentreByName(theme)                            
 
    def _find_topic(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = { 'portal_type': ('Topic', 'RichTopic'),
                  'path': '/'.join(self.themecentre.getPhysicalPath()) }
        brains = catalog.searchResults(query)
        topics = [brain.getObject() for brain in brains]
        for topic in topics:
            if 'crit__Type_ATPortalTypeCriterion' in topic.objectIds():
                criteria = topic.getCriterion('Type_ATPortalTypeCriterion')
                if self.context.archetype_name in criteria.Value():
                    return topic
        return None

    def url(self, theme):
        self.themecentre = self._themecentre(theme)
        if self.themecentre is None:
            return ''
        
        topic = self._find_topic()
        if topic:
            return topic.absolute_url()
        else:
            portal_type = self.context.portal_type
            return self.themecentre.absolute_url() + \
                    '/contentbytype?contenttype=' + portal_type

class MediaLink(LinkAdapter):
    def url(self, theme):
         return self._themecentre(theme).absolute_url() + '/multimedia' 
