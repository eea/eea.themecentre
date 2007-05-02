from zope.app.component.hooks import getSite
from zope.app.event.objectevent import ObjectEvent
from zope.app.traversing.interfaces import ITraverser
from zope.component import adapts
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Acquisition import aq_parent

from eea.themecentre.interfaces import IThemeTagging, IThemeCentre
from eea.themecentre.interfaces import IThemeCentreSchema
from eea.themecentre.vocabulary import ThemesVocabularyFactory

RDF_THEME_KEY = 'eea.themecentre.rdf'

class PromotedToThemeCentreEvent(ObjectEvent):
    """ A theme tag has been added to an object. """

def promoted(obj, event):
    # no AT field is changed on the object, so noone else knows that the
    # folder should be reindexed because of the new interface we added
    obj.reindexObject()

    workflow = getToolByName(obj, 'portal_workflow')

    # obj should be a folder and that's where we're gonna add a news folder
    obj.invokeFactory('Folder', id='news', title='News')
    obj.invokeFactory('Folder', id='events', title='Events')
    obj.invokeFactory('Folder', id='links', title='Links')
    obj.invokeFactory('HelpCenterFAQFolder', id='faq', title='FAQ')
    obj.invokeFactory('Folder', id='multimedia', title='Multimedia')
    multimedia = getattr(obj, 'multimedia')
    multimedia.layout = 'mediacentre_view'
    multimedia.exclude_from_nav = True
    workflow.doActionFor(multimedia, 'publish')

    newsobj = getattr(obj, 'news', None)
    eventsobj = getattr(obj, 'events', None)
    linksobj = getattr(obj, 'links', None)
    faqobj = getattr(obj, 'faq', None)

    if newsobj:
        workflow.doActionFor(newsobj, 'publish')
        newsobj.setConstrainTypesMode(1)
        newsobj.setImmediatelyAddableTypes(['News Item'])
        newsobj.setLocallyAllowedTypes(['News Item'])
        newsobj.layout = 'folder_listing'
        
    if eventsobj:
        workflow.doActionFor(eventsobj, 'publish')
        eventsobj.setConstrainTypesMode(1)
        eventsobj.setImmediatelyAddableTypes(['Event'])
        eventsobj.setLocallyAllowedTypes(['Event'])
        eventsobj.layout = 'folder_listing'
        
    if linksobj:
        workflow.doActionFor(linksobj, 'publish')
        linksobj.setConstrainTypesMode(1)
        linksobj.setImmediatelyAddableTypes(['Link'])
        linksobj.setLocallyAllowedTypes(['Link'])
        linksobj.layout = 'folder_listing'
        

def objectAdded(obj, event):
    """ Checks if the object belongs to a theme centre. If it does and it
        is taggable, then it is tagged with the current theme. """

    if IThemeCentre.providedBy(obj):
        return

    themeCentre = getThemeCentre(obj)
    if themeCentre:
        themes = IThemeTagging(obj, None)
        if themes:
            themeCentreThemes = IThemeCentreSchema(themeCentre)
            themes.tags = [themeCentreThemes.tags]

def objectThemeTagged(obj, event):
    """ Checks if the object's theme tags are modified. If true, catalog
        is updated. """

    portal_catalog = getToolByName(getSite(), 'portal_catalog')
    for desc in event.descriptions:
        if desc.interface == IThemeTagging:
            portal_catalog.reindexObject(obj)

def getThemeCentre(context):
    """ Looks up the closest theme centre. """

    while context and not IPloneSiteRoot.providedBy(context) and \
          not IThemeCentre.providedBy(context):
        context = aq_parent(context)

    if IThemeCentre.providedBy(context):
        return context
    else:
        return None

def getTheme(context):
    themeCentre = getThemeCentre(context)

    if IThemeCentre.providedBy(themeCentre):
        themes = IThemeCentreSchema(themeCentre)

        if themes:
            return themes.tags

    return None

class O:
    pass

def getThemeTitle(context):
    themeid = getTheme(context)
    if themeid:
        o = O()
        o.context = context
        vocab = ThemesVocabularyFactory(o)
        return vocab.getTerm(themeid).title
    return None

#class RDFTraversalAdapter(FiveTraversable):
#    implements(ITraverser)
#    adapts(IThemeCentre)
#
#    def publishTraverse(self, request, name):
#        return 'woo'
