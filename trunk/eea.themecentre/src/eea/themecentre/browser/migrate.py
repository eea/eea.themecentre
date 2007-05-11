import urllib
from zope.interface import alsoProvides, directlyProvides, directlyProvidedBy
from eea.themecentre.interfaces import IThemeCentreSchema, IThemeRelation, IThemeTagging
from eea.themecentre.browser.themecentre import PromoteThemeCentre
from eea.rdfrepository.interfaces import IFeed, IFeedContent
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.interfaces import INavigationRoot
import socket
import feedparser

url = 'http://themes.eea.europa.eu/migrate/%s?theme=%s'

# Some new theme ids are not same as old
themeIdMap = { 'coasts_seas' : 'coast_sea',
               'fisheries' : 'fishery',
               'human_health' : 'human',
               'natural_resources' : 'natural',
               'env_information' : 'information',
               'env_management' : 'management',
               'env_reporting' : 'reporting',
               'env_scenarios' : 'scenarios',
               'various' : 'other_issues' }

class FixExcludeFromNav(object):
    """ fix overwritten exclude_from_nav """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context
        res = context.portal_catalog.searchResults(portal_type = 'Folder', id='multimedia', path = '/'.join(context.getPhysicalPath()))
        for folder in res:
            obj = folder.getObject()
            if hasattr(aq_base(obj), 'exclude_from_nav'):
                del obj.exclude_from_nav
                obj.initializeLayers()
            
class MigrateWrongThemeIds(object):
    """ migrate wrong theme ids to old correct """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context
        themeVocab = context.portal_vocabularies.themes         
        themeIds = themeVocab.objectIds()

        for theme in themeIdMap.keys():
            res = context.portal_catalog.searchResults(getThemes=theme)
            for r in res:
                obj = r.getObject()
                try:
                    currentThemes = obj.getThemes()
                except:
                    continue
                if currentThemes == str(currentThemes):
                    currentThemes = [currentThemes,]
                newThemes = [ themeIdMap.get(r,r) for r in currentThemes ]
                obj.setThemes(newThemes)
                print '%s: %s -> %s' % (obj, currentThemes, newThemes) 

        for t in themeIds:
            newT = themeIdMap.get(t,t)
            if newT != t:
                obj = themeVocab[t]
                obj.setId(newT)

class MigrateTheme(object):
    """ Migrate theme info from themes.eea.europa.eu zope 2.6.4 """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        newThemeId = self.context.getId()
        themeId = themeIdMap.get(newThemeId, newThemeId)
        try:
            step = 0
            self._title(themeId)
            step += 1            
            self._intro(themeId)
            step += 1
            self._relatedThemes(themeId)
            step += 1
            self._links(themeId)
            step += 1
            self._image(themeId)
            step += 1
            self._indicators(themeId)            
        except:
            print themeId + ' failed on step %s' % step
        self.context.reindexObject()
        
    def _title(self, themeId):
        titleUrl = url % ('themeTitle', themeId)
        title = urllib.urlopen(titleUrl).read()
        title = title.replace('\n','')
        self.context.setTitle(title)

    def _image(self, themeId):
        getUrl = url % ('themeUrl', themeId)
        themeUrl  = urllib.urlopen(getUrl).read().strip()
        imageUrl = themeUrl + '/theme_image'
        imageData  = urllib.urlopen(imageUrl).read().strip()
        image = self.context.invokeFactory('Image', id='theme_image', title='%s - Theme image' % self.context.Title())
        obj = self.context[image]
        obj.setImage(imageData)
        obj.reindexObject()
        
    def _relatedThemes(self, themeId):
        relatedUrl = url % ('themeRelated', themeId)
        related = urllib.urlopen(relatedUrl).read().strip()
        related = related[1:-1].replace('\'','')
        related = [ theme.strip() for theme in related.split(',') ]
        theme = IThemeRelation(self.context)
        themeCentres = self.context.portal_catalog.searchResults(object_provides='eea.themecentre.interfaces.IThemeCentre')
        tcs = {}
        for tc in themeCentres:
            tcs[tc.getId] =  tc.getObject().UID()
        themeCentres = tcs

        # map old theme id to new
        related = [ themeIdMap.get(r, r) for r in related ]
        
        # XXX need to find UID for the related theme centres
        related = [ themeCentres.get(r) for r in related ]
        related = [ r for r in related
                      if r is not None ]
        theme.related = related

    def _intro(self, themeId):
        introUrl = url % ('themeIntro', themeId)
        introText = urllib.urlopen(introUrl).read().strip()
        intro = 'intro'
        if not hasattr(self.context, intro):
            intro = self.context.invokeFactory('Document', id=intro)
            obj = self.context[intro]
            obj.setTitle(self.context.Title() + ' introduction')
            obj.setText(introText, mimetype='text/html')
            obj.reindexObject()

    def _links(self, themeId):
        workflow = getToolByName(self.context, 'portal_workflow')        
        linksUrl = url % ('themeLinks', themeId)
        links = urllib.urlopen(linksUrl).read().strip()
        links = links.split('\n')
        folder = self.context.links
        for link in links:
            link = link.split(';')
            if not link[0].strip():
                continue
            linkId = folder.invokeFactory('Link', id=link[0].strip())
            obj = folder[linkId]
            try:
                obj.setTitle(link[1].strip().decode('iso-8859-1'))
            except:
                obj.setTitle('link[2].strip()')
            obj.setRemoteUrl(link[2].strip())
            workflow.doActionFor(obj, 'publish')

    def _indicators(self, themeId):
        workflow = getToolByName(self.context, 'portal_workflow')        
        indiUrl = url % ('themeIndicator', themeId)
        indiText = urllib.urlopen(indiUrl).read().strip()
        indicators = 'indicators'
        if not hasattr(self.context, indicators):
            indicators = self.context.invokeFactory('Document', id=indicators)
            obj = self.context[indicators]
            obj.setTitle('Indicators')
            obj.setText(indiText, mimetype='text/html')
            catalog = getToolByName(self.context, 'portal_catalog')        
            indicatorRSS = catalog.searchResults( portal_type='RSSFeedRecipe', id='indicators_' +themeId)
            if len(indicatorRSS) > 0:
                obj.setRelatedItems(indicatorRSS[0].getObject().UID())
            workflow.doActionFor(obj, 'publish')            
            obj.reindexObject()

        
class InitialThemeCentres(object):
    """ create inital theme structure """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context
        workflow = getToolByName(self.context, 'portal_workflow')
        fixThemeIds = MigrateWrongThemeIds(context, self.request)
        fixThemeIds()
        
        themeids = context.portal_vocabularies.themes.objectIds()[1:]
        noThemes = int(self.request.get('noThemes',0))
        if noThemes > 0:
            themeids = themeids[:noThemes]
        toMigrate = self.request.get('migrate', False)
        for theme in themeids:
            if not hasattr(aq_base(context), theme):
                folder = context.invokeFactory('Folder', id=theme, title=theme)
                folder = context[folder]
                ptc = PromoteThemeCentre(folder, self.request)
                ptc(theme)
                workflow.doActionFor(folder, 'publish')

        if toMigrate:
            for theme in themeids:
                tc = context[theme]
                migrate = MigrateTheme(tc, self.request)
                migrate()

        if not hasattr(aq_base(context), 'right_slots'):
            slots = ['here/portlet_themes_related/macros/portlet',
                     'here/portlet_themes_rdf/macros/portlet']
            context.manage_addProperty('right_slots', slots, type='lines')

        if not hasattr(aq_base(context), 'left_slots'):
            slots = ['here/portlet_themes/macros/portlet', ]
            context.manage_addProperty('left_slots', slots, type='lines',),

        #if hasattr(aq_base(context), 'navigationmanager_menuid'):
        #    context.manage_addProperty('navigationmanager_menuid', 'themes', type='string')

        alsoProvides(context, INavigationRoot)
        context.layout = 'themes_view'
        return self.request.RESPONSE.redirect(context.absolute_url())

class RDF(object):
    """ Copies RDF/RSS feeds from themes.eea.europa.eu to
        RSSFeedRecipe objects in the current folder. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        socket.setdefaulttimeout(15)
        workflow = getToolByName(self.context, 'portal_workflow')
        migrate_url = url % ('themeRDF', '')
        feeds = urllib.urlopen(migrate_url).readlines()

        for feed_line in feeds:
            id, title, feed_url = feed_line.split('|')
            if id.startswith("reports_"):
                title = "Reports"
            elif not title:
                title = id

            self.context.invokeFactory('RSSFeedRecipe', id=id, title=title)
            recipe = self.context[id]
            recipe.setEntriesSize(10000)
            recipe.setFeedURL(feed_url)
            recipe.setEntriesWithDescription(0)
            recipe.setEntriesWithThumbnail(0)

            parsed = feedparser.parse(feed_url)
            if parsed['feed'].has_key('link'):
                recipe.setUrl(parsed['feed']['link'])

            x = feed_url.find('theme=')
            if x > -1:
                theme = feed_url[x+6:].strip()
                taggable = IThemeTagging(recipe)
                taggable.tags = [theme]

            workflow.doActionFor(recipe, 'publish')


        return str(len(feeds)) + ' RDF/RSS files were successfully migrated.'

class IndicatorRDFs(object):
    """ Create RSSFeedRecipes for indicator rss """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context
        workflow = getToolByName(self.context, 'portal_workflow')
        url = 'http://themes.eea.europa.eu/indicators/bytheme.rss?theme_id=%s'
        themeids = context.portal_vocabularies.themes.objectIds()[1:]
        for theme in themeids:
            feedId = 'indicators_%s' % theme
            title = 'Indicators'
            feed_url = url % theme
            self.context.invokeFactory('RSSFeedRecipe', id=feedId, title=title)
            recipe = self.context[feedId]
            recipe.setEntriesSize(10000)
            recipe.setFeedURL(feed_url)

            taggable = IThemeTagging(recipe)
            taggable.tags = [theme]

            workflow.doActionFor(recipe, 'publish')
            recipe.reindexObject()
            
        return str(len(themeids)) + ' indicator fees created.'
    
class ThemeTaggable(object):
    """ Migrate theme tags to anootations. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        types = ('Highlight', 'Promotion', 'QuickEvent', 'PressRelease',
                'Speech')
        brains = catalog.searchResults(portal_type=types)

        for brain in brains:
            obj = brain.getObject()
            tagging = IThemeTagging(obj)
            themes = filter(None, obj.schema['themes'].get(obj))
            tagging.tags = themes

class EventsTopicEndDate(object):
    """ Change all event topics to have end instead of start in criteria. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = { 'portal_type': 'Topic',
                  'id': 'events_topic' }
        brains = catalog.searchResults(query)
        for brain in brains:
            topic = brain.getObject()
            if 'crit__start_ATFriendlyDateCriteria' in topic.objectIds():
                topic.deleteCriterion('crit__start_ATFriendlyDateCriteria')

            if 'crit__end_ATFriendlyDateCriteria' not in topic.objectIds():
                date_crit = topic.addCriterion('end', 'ATFriendlyDateCriteria')
                date_crit.setValue(0)
                date_crit.setDateRange('+')
                date_crit.setOperation('more')
        return 'success'

class FeedMarkerInterface(object):
    """ Changes all IFeed marker interfaces to be IFeedContent markers. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = { 'portal_type': 'RSSFeedRecipe' }
        brains = catalog.searchResults(query)
        for brain in brains:
            feed = brain.getObject()
            directlyProvides(feed, directlyProvidedBy(feed)-IFeed)
            directlyProvides(feed, directlyProvidedBy(feed), IFeedContent)
            feed.reindexObject()
        return 'success'
