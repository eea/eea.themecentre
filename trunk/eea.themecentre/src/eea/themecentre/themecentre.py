from zope.app.component.hooks import getSite
from zope.app.event.objectevent import ObjectEvent
from zope.app.traversing.interfaces import ITraverser
from zope.component import adapts
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

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
    obj.invokeFactory('Folder', id='highlights', title='Highlights')
    obj.invokeFactory('Folder', id='events', title='Events')
    obj.invokeFactory('Folder', id='links', title='External Links')
    obj.invokeFactory('HelpCenterFAQFolder', id='faq', title='FAQ')
    obj.invokeFactory('Folder', id='multimedia', title='Multimedia')
    multimedia = getattr(obj, 'multimedia')
    multimedia.layout = 'mediacentre_view'
    multimedia.exclude_from_nav = True
    workflow.doActionFor(multimedia, 'publish')

    newsobj = getattr(obj, 'highlights', None)
    eventsobj = getattr(obj, 'events', None)
    linksobj = getattr(obj, 'links', None)
    faqobj = getattr(obj, 'faq', None)

    theme_id = IThemeCentreSchema(obj).tags

    if newsobj:
        workflow.doActionFor(newsobj, 'publish')
        newsobj.setConstrainTypesMode(1)
        newsobj.setImmediatelyAddableTypes(['News Item'])
        newsobj.setLocallyAllowedTypes(['News Item'])
        newsobj.default_page = 'highlights_topic'

        # add a smart folder to the news folder that shows all news and
        # highlighs
        _createObjectByType('Topic', newsobj, id='highlights_topic',
                title='Highlights')
        topic = getattr(newsobj, 'highlights_topic')
        type_crit = topic.addCriterion('Type', 'ATPortalTypeCriterion')
        type_crit.setValue(['News Item', 'Highlight'])
        sort_crit = topic.addCriterion('created', 'ATSortCriterion')
        state_crit = topic.addCriterion('review_state',
                                        'ATSimpleStringCriterion')
        state_crit.setValue('published')
        theme_crit = topic.addCriterion('getThemes',
                                        'ATSimpleStringCriterion')
        theme_crit.setValue(theme_id)
        effective_crit = topic.addCriterion('effective', 'ATFriendlyDateCriteria')
        effective_crit.setOperation('less')
        effective_crit.setValue(0)
        
        topic.setSortCriterion('effective', True)
        topic.setLayout('atct_topic_view')
        
    if eventsobj:
        workflow.doActionFor(eventsobj, 'publish')
        eventsobj.setConstrainTypesMode(1)
        eventsobj.setImmediatelyAddableTypes(['Event'])
        eventsobj.setLocallyAllowedTypes(['Event'])
        eventsobj.default_page = 'events_topic'
        
        # add a smart folder to the events folder that shows all events
        _createObjectByType('Topic', eventsobj, id='events_topic', title='Events')
        topic = getattr(eventsobj, 'events_topic')
        type_crit = topic.addCriterion('Type', 'ATPortalTypeCriterion')
        type_crit.setValue(('Event','QuickEvent', 'RDFEvent'))
        sort_crit = topic.addCriterion('created', 'ATSortCriterion')
        state_crit = topic.addCriterion('review_state',
                                        'ATSimpleStringCriterion')
        state_crit.setValue('published')
        theme_crit = topic.addCriterion('getThemes',
                                        'ATSimpleStringCriterion')
        theme_crit.setValue(theme_id)
        date_crit = topic.addCriterion('start', 'ATFriendlyDateCriteria')
        date_crit.setValue(0)
        date_crit.setDateRange('+')
        date_crit.setOperation('more')
        topic.setLayout('atct_topic_view')

    if linksobj:
        workflow.doActionFor(linksobj, 'publish')
        linksobj.setConstrainTypesMode(1)
        linksobj.setImmediatelyAddableTypes(['Link'])
        linksobj.setLocallyAllowedTypes(['Link'])
        linksobj.default_page = 'links_topic'
        
        # add a smart folder to the links folder that shows all links
        _createObjectByType('Topic', linksobj, id='links_topic', title='Links')
        topic = getattr(linksobj, 'links_topic')
        type_crit = topic.addCriterion('Type', 'ATPortalTypeCriterion')
        type_crit.setValue('Link')
        sort_crit = topic.addCriterion('created', 'ATSortCriterion')
        state_crit = topic.addCriterion('review_state',
                                        'ATSimpleStringCriterion')
        state_crit.setValue('published')
        theme_crit = topic.addCriterion('getThemes',
                                        'ATSimpleStringCriterion')
        theme_crit.setValue(theme_id)
        topic.setSortCriterion('effective', True)
        topic.setLayout('atct_topic_view')


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

    site = getSite()
    if site is None:
        return
    
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
