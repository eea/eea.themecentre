""" Theme centre module
"""
from zope.app.component.hooks import getSite
from zope.component.interfaces import ObjectEvent
from zope.component import adapter
from zope.interface import Interface, implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.EEAPloneAdmin.browser.interfaces import IObjectTitle
from Acquisition import aq_parent, aq_base
from eea.themecentre.interfaces import IThemeTagging, IThemeCentre
from eea.themecentre.interfaces import IThemeCentreSchema
from eea.themecentre.interfaces import IThemeCentreImageUrl
from eea.themecentre.vocabulary import ThemesVocabularyFactory

RDF_THEME_KEY = 'eea.themecentre.rdf'

class PromotedToThemeCentreEvent(ObjectEvent):
    """ A theme tag has been added to an object.
    """

def promoted(obj, event):
    """ No AT field is changed on the object, so noone else knows that the
        folder should be reindexed because of the new interface we added
    """
    obj.reindexObject()

    workflow = getToolByName(obj, 'portal_workflow')
    # obj should be a folder and that's where we're gonna add a news folder
    obj.invokeFactory('Folder', id='highlights', title='Highlights')
    obj.invokeFactory('Folder', id='events', title='Upcoming events')
    obj.invokeFactory('Folder', id='links', title='External links')
    obj.invokeFactory('HelpCenterFAQFolder', id='faq', title='FAQ')
    obj.invokeFactory('Folder', id='multimedia', title='Multimedia')
    multimedia = getattr(obj, 'multimedia')
    multimedia.setLayout('mediacentre_view')
    multimedia.setExcludeFromNav(True)
    multimedia.processForm()
    workflow.doActionFor(multimedia, 'publish')

    newsobj = getattr(obj, 'highlights', None)
    newsobj._at_rename_after_creation = False
    newsobj.processForm()
    eventsobj = getattr(obj, 'events', None)
    eventsobj._at_rename_after_creation = False
    eventsobj.processForm()
    linksobj = getattr(obj, 'links', None)
    linksobj._at_rename_after_creation = False
    linksobj.processForm()
    faqobj = getattr(obj, 'faq', None)
    faqobj._at_rename_after_creation = False
    faqobj.processForm()

    theme_id = IThemeCentreSchema(obj).tags
    obj.invokeFactory('Document',
                      id='intro',
                      title=obj.Title() + ' introduction')
    if not hasattr(aq_base(obj), 'default_page'):
        obj.manage_addProperty('default_page', 'intro', 'string')
    intro = getattr(obj, 'intro')
    intro.manage_addProperty('layout', 'themecentre_view', 'string')
    # we must turn off rename otherwise it will be renamed to 'introduction'
    intro._at_rename_after_creation = False
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
        type_crit.setValue(['News Item', 'Highlight', 'Press Release'])
        topic.addCriterion('created', 'ATSortCriterion')
        state_crit = topic.addCriterion('review_state',
                                        'ATSimpleStringCriterion')
        state_crit.setValue('published')
        theme_crit = topic.addCriterion('getThemes',
                                        'ATSimpleStringCriterion')
        theme_crit.setValue(theme_id)
        effective_crit = topic.addCriterion('effective',
                                            'ATFriendlyDateCriteria')
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
        type_crit.setValue(('Event', 'QuickEvent'))
        topic.addCriterion('start', 'ATSortCriterion')
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
        linksobj.setImmediatelyAddableTypes(['Folder', 'Link'])
        linksobj.setLocallyAllowedTypes(['Folder', 'Link'])
        linksobj.manage_addProperty('default_page', 'links_topic',
                                   'string')

        # add a smart folder to the links folder that shows all links
        _createObjectByType('Topic', linksobj, id='links_topic',
                            title='External links')
        topic = getattr(linksobj, 'links_topic')
        type_crit = topic.addCriterion('Type', 'ATPortalTypeCriterion')
        type_crit.setValue('Link')
        topic.addCriterion('created', 'ATSortCriterion')
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
    """ Add a smart folder to the faq folder that shows all faqs
    """
    _createObjectByType('Topic', parent, id='faqs_topic',
                        title='FAQ')
    topic = getattr(parent, 'faqs_topic')
    type_crit = topic.addCriterion('Type', 'ATPortalTypeCriterion')
    type_crit.setValue('FAQ')
    topic.addCriterion('created', 'ATSortCriterion')
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
    """ IObjectMovedEvent is a very generic event, so we have to check
        source and destination to make sure it's really a cut & paste
    """
    if event.oldParent is not None and event.newParent is not None:
        objectAdded(obj, event)

def objectThemeTagged(obj, event):
    """ Checks if the object's theme tags are modified. If true, tags are
        copied to eventual translations, and catalog is updated.
    """
    for desc in event.descriptions:
        if desc.interface == IThemeTagging:
            try:
                context = obj.context
            except AttributeError:
                context = obj

            if context.isCanonical():
                for _lang, trans in context.getTranslations().items():
                    IThemeTagging(trans[0]).tags = IThemeTagging(context).tags
            context.reindexObject()

def getThemeCentre(context):
    """ Looks up the closest theme centre.
    """
    count = 0

    while context and not IPloneSiteRoot.providedBy(context) and \
          not IThemeCentre.providedBy(context):

        #TODO: plone4 migration
        # If type(context) == 'plone.keyring.keyring.Keyring'
        #  enters a infinite cycle or
        #  context is <plone.app.portlets.portlets.navigation ..
        # Below there are some cases trated not to enter a infinite cycle.
        # This happens only on tests.
        count += 1
        if count == 50:
            break
        context_id = getattr(context, 'getId', None)
        if context_id:
            context_id = context_id()
            if context_id in ['navigation']:
                break
            elif '++' in context_id:
                break
        if context == [None, None, None, None]:
            break

        context = aq_parent(context)

    if IThemeCentre.providedBy(context):
        return context
    else:
        return None

def getThemeCentreByName(name):
    """ Get Theme Centre by Name
    """
    catalog = getToolByName(getSite(), 'portal_catalog')
    brains = catalog.searchResults(
            Language='en',
            object_provides=IThemeCentre.__identifier__,
            getThemes=name)
    if brains:
        tc = brains[0].getObject()
        lang = catalog.REQUEST.get('LANGUAGE', 'en')
        if lang != 'en':
            tcTranslation = tc.getTranslation(lang)
            if tcTranslation is not None:
                tc = tcTranslation
        return tc
    else:
        return None

def getTheme(context):
    """ Get theme
    """
    themeCentre = getThemeCentre(context)

    if IThemeCentre.providedBy(themeCentre):
        themes = IThemeCentreSchema(themeCentre)

        if themes:
            return themes.tags

    return None

class O:
    """ Dummy class
    """
    pass

def getThemeTitle(context):
    """ Get Theme Title
    """
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
    return None

@implementer(IThemeCentreImageUrl)
@adapter(IThemeCentre)
def imageUrl(context):
    """ An adapter that checks if the translation has an theme_image if not it
        returns the url to the canonical theme centre image. """

    tc = context
    if not hasattr(tc, 'theme_image'):
        tc = context.getCanonical()
    image = getattr(tc, 'theme_image', None)
    if image:
        return '%s/image_icon' % image.absolute_url()
    else:
        return ''
