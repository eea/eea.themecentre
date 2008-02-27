from zope.app.component.hooks import getSite
from zope.app.event.objectevent import ObjectEvent
from zope.component import adapter
from zope.interface import implements, Interface, implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.EEAPloneAdmin.browser.interfaces import IObjectTitle
from Acquisition import aq_parent, aq_base

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
    obj.invokeFactory('Folder', id='events', title='Upcoming events')
    obj.invokeFactory('Folder', id='links', title='External links')
    obj.invokeFactory('HelpCenterFAQFolder', id='faq', title='FAQ')
    obj.invokeFactory('Folder', id='multimedia', title='Multimedia')
    multimedia = getattr(obj, 'multimedia')
    multimedia.layout = 'mediacentre_view'
    multimedia.setExcludeFromNav(True)
    multimedia.processForm()
    workflow.doActionFor(multimedia, 'publish')

    newsobj = getattr(obj, 'highlights', None)
    newsobj.processForm()
    eventsobj = getattr(obj, 'events', None)
    eventsobj.processForm()
    linksobj = getattr(obj, 'links', None)
    linksobj.processForm()
    faqobj = getattr(obj, 'faq', None)
    faqobj.processForm()

    theme_id = IThemeCentreSchema(obj).tags

    obj.invokeFactory('Document', id='intro', title=obj.Title()+' introduction')
    if not hasattr(aq_base(obj), 'default_page'):
        obj.manage_addProperty('default_page', 'intro', 'string')
    intro = getattr(obj, 'intro')
    intro.manage_addProperty('layout', 'themecentre_view', 'string')
    intro.processForm()

    if newsobj:
        workflow.doActionFor(newsobj, 'publish')
        newsobj.setConstrainTypesMode(1)
        newsobj.setImmediatelyAddableTypes(['News Item'])
        newsobj.setLocallyAllowedTypes(['News Item'])
        newsobj.manage_addProperty('default_page', 'highlights_topic',
                                   'string')

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
        topic.setCustomViewFields(['EffectiveDate'])
        topic._at_rename_after_creation = False
        
    if eventsobj:
        workflow.doActionFor(eventsobj, 'publish')
        eventsobj.setConstrainTypesMode(1)
        eventsobj.setImmediatelyAddableTypes(['Event'])
        eventsobj.setLocallyAllowedTypes(['Event'])
        eventsobj.manage_addProperty('default_page', 'events_topic',
                                   'string')
        
        # add a smart folder to the events folder that shows all events
        _createObjectByType('Topic', eventsobj, id='events_topic',
                            title='Upcoming events')
        topic = getattr(eventsobj, 'events_topic')
        type_crit = topic.addCriterion('Type', 'ATPortalTypeCriterion')
        type_crit.setValue(('Event','QuickEvent', 'RDFEvent'))
        sort_crit = topic.addCriterion('start', 'ATSortCriterion')
        state_crit = topic.addCriterion('review_state',
                                        'ATSimpleStringCriterion')
        state_crit.setValue('published')
        theme_crit = topic.addCriterion('getThemes',
                                        'ATSimpleStringCriterion')
        theme_crit.setValue(theme_id)
        date_crit = topic.addCriterion('end', 'ATFriendlyDateCriteria')
        date_crit.setValue(0)
        date_crit.setDateRange('+')
        date_crit.setOperation('more')
        topic.setLayout('atct_topic_view')
        topic.setCustomViewFields(['start', 'end', 'location'])
        topic._at_rename_after_creation = False

    if linksobj:
        workflow.doActionFor(linksobj, 'publish')
        linksobj.setConstrainTypesMode(1)
        linksobj.setImmediatelyAddableTypes(['Link'])
        linksobj.setLocallyAllowedTypes(['Link'])
        linksobj.manage_addProperty('default_page', 'links_topic',
                                   'string')
        
        # add a smart folder to the links folder that shows all links
        _createObjectByType('Topic', linksobj, id='links_topic',
                            title='External links')
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
        topic.setCustomViewFields([])
        topic._at_rename_after_creation = False

    if faqobj:
        createFaqSmartFolder(faqobj, theme_id)

def createFaqSmartFolder(parent, theme_id):
        # add a smart folder to the faq folder that shows all faqs
        _createObjectByType('Topic', parent, id='faqs_topic',
                            title='FAQ')
        topic = getattr(parent, 'faqs_topic')
        type_crit = topic.addCriterion('Type', 'ATPortalTypeCriterion')
        type_crit.setValue('FAQ')
        sort_crit = topic.addCriterion('created', 'ATSortCriterion')
        state_crit = topic.addCriterion('review_state',
                                        'ATSimpleStringCriterion')
        state_crit.setValue('published')
        theme_crit = topic.addCriterion('getThemes',
                                        'ATSimpleStringCriterion')
        theme_crit.setValue(theme_id)
        topic.setSortCriterion('effective', True)
        topic.setLayout('atct_topic_view')
        topic.setCustomViewFields([])
        topic._at_rename_after_creation = False


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
            if themeCentreThemes.tags not in themes.tags:
                themes.tags += [themeCentreThemes.tags]

def objectMoved(obj, event):
    # IObjectMovedEvent is a very generic event, so we have to check
    # source and destination to make sure it's really a cut & paste
    if event.oldParent is not None and event.newParent is not None:
       objectAdded(obj, event)

def objectThemeTagged(obj, event):
    """ Checks if the object's theme tags are modified. If true, catalog
        is updated. """

    site = getSite()
    if site is None:
        return

    portal_catalog = getToolByName(site, 'portal_catalog')
    for desc in event.descriptions:
        if desc.interface == IThemeTagging:
            portal_catalog.reindexObject(obj.context)

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

@implementer(IObjectTitle)
@adapter(Interface, IBrowserRequest)
def objectTitle(context, request):
    """ An adapter that gets the title from the current object/template.
        It's used for instance for showing title in the web browser title
        bar. If the request has 'feed' variable then the feed's title
        is used, otherwise some other adapter is used instead. """

    class ObjectTitle(object):
        implements(IObjectTitle)
        def __init__(self, title):
            self._title = title
        @property
        def title(self):
            return self._title

    feed = request.get('feed', None)
    if feed:
        portal_catalog = getToolByName(context, 'portal_catalog')
        # TODO use refactored rdf repository and interfaces instead of catalog
        brains = portal_catalog.searchResults(id=feed,
                portal_type='RSSFeedRecipe')
        if brains:
            putils = getToolByName(context, 'plone_utils')
            object_title = putils.pretty_title_or_id(context)
            return ObjectTitle('%s - %s' % (brains[0].Title, object_title))
        else:
            return None
    else:
        return None
