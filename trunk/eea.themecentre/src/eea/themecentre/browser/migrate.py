import urllib
from zope.interface import alsoProvides, directlyProvides, directlyProvidedBy
from eea.themecentre.interfaces import IThemeCentreSchema, IThemeRelation
from eea.themecentre.interfaces import IThemeTagging, IThemeCentre
from eea.themecentre.browser.themecentre import PromoteThemeCentre
from eea.themecentre.themecentre import createFaqSmartFolder, getThemeCentre
from eea.rdfrepository.interfaces import IFeed, IFeedContent
from eea.mediacentre.interfaces import IMediaType
from p4a.video.interfaces import IVideo
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.interfaces import INavigationRoot
import socket
import feedparser
import urlparse

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
            exclude_from_nav = getattr(aq_base(obj), 'exclude_from_nav', None)
            if exclude_from_nav and not callable(exclude_from_nav):
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
                ptc()

                tc = IThemeCentreSchema(folder)
                tc.tags = theme

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
            id, title, feed_url = feed_line.strip().split('|')
            if id.startswith("reports_"):
                title = "Reports"
            elif not title:
                title = id

            if not hasattr(self.context, id):
                self.context.invokeFactory('RSSFeedRecipe', id=id, title=title)

            recipe = self.context[id]
            recipe.setEntriesWithDescription(0)
            recipe.setEntriesWithThumbnail(0)

            parsed = feedparser.parse(feed_url)
            if parsed['feed'].has_key('link'):
                recipe.setUrl(parsed['feed']['link'])

            recipe.setEntriesSize(10000)

            x = feed_url.find('theme=')
            if x > -1:
                theme = feed_url[x+6:].strip()
                taggable = IThemeTagging(recipe)
                taggable.tags = [theme]

            parsed_url = urlparse.urlparse(feed_url)
            if parsed_url[2] != '/schema.rdf' and parsed_url[2].endswith('.rdf'):
                if parsed_url[4]:
                    feed_url += '&image=yes'
                else:
                    feed_url += '?image=yes'
            recipe.setFeedURL(feed_url)

            if workflow.getInfoFor(recipe, 'review_state') != \
                    'published':
                workflow.doActionFor(recipe, 'publish')
            recipe.reindexObject()


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
            if not hasattr(self.context, feedId):
                self.context.invokeFactory('RSSFeedRecipe', id=feedId, title=title)
            recipe = self.context[feedId]
            recipe.setEntriesSize(10000)
            recipe.setFeedURL(feed_url)
            recipe.setEntriesWithDescription(0)
            recipe.setEntriesWithThumbnail(0)

            parsed = feedparser.parse(feed_url)
            if parsed['feed'].has_key('link'):
                recipe.setUrl(parsed['feed']['link'])

            taggable = IThemeTagging(recipe)
            taggable.tags = [theme]

            if workflow.getInfoFor(recipe, 'review_state') != \
                    'published':
                workflow.doActionFor(recipe, 'publish')
            recipe.reindexObject()
            
        return str(len(themeids)) + ' indicator fees migrated.'
    
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

class UpdateSmartFoldersAndTitles(object):
    """ Change all event topics to have end instead of start in criteria. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        # change criteria on event topic
        query = { 'portal_type': 'Topic',
                  'id': 'events_topic' }
        brains = catalog.searchResults(query)
        for brain in brains:
            topic = brain.getObject()
            topic.setTitle('Upcoming events')
            topic.reindexObject()

            if 'crit__start_ATFriendlyDateCriteria' in topic.objectIds():
                topic.deleteCriterion('crit__start_ATFriendlyDateCriteria')

            if 'crit__end_ATFriendlyDateCriteria' not in topic.objectIds():
                date_crit = topic.addCriterion('end', 'ATFriendlyDateCriteria')
                date_crit.setValue(0)
                date_crit.setDateRange('+')
                date_crit.setOperation('more')

            if 'crit__created_ATSortCriterion' in topic.objectIds():
                topic.deleteCriterion('crit__created_ATSortCriterion')
                topic.addCriterion('start', 'ATSortCriterion')

            # add custom fields to the events and highlight folders, links don't
            # need any as they shouldn't show anything in "detail"
            topic.setCustomViewFields(['start', 'end', 'location'])

        # add custom field on all highligh topic
        query = { 'portal_type': 'Topic',
                  'id': 'highlights_topic' }
        brains = catalog.searchResults(query)
        for brain in brains:
            topic = brain.getObject()
            topic.setCustomViewFields(['EffectiveDate'])

        # remove custom field on all link topics
        query = { 'portal_type': 'Topic',
                  'id': 'links_topic' }
        brains = catalog.searchResults(query)
        for brain in brains:
            topic = brain.getObject()
            topic.setTitle('External links')
            topic.reindexObject()
            topic.setCustomViewFields([])

        # rename titles on folders in themecentre
        query = { 'object_provides': 'eea.themecentre.interfaces.IThemeCentre' }
        brains = catalog.searchResults(query)
        for brain in brains:
            themecentre = brain.getObject()

            events_folder = getattr(themecentre, 'events')
            if events_folder:
                events_folder.setTitle('Upcoming events')
                events_folder.reindexObject()
            links_folder = getattr(themecentre, 'links')
            if links_folder:
                links_folder.setTitle('External links')
                links_folder.reindexObject()

            faqs_folder = getattr(themecentre, 'faq')
            if faqs_folder:
                if not getattr(faqs_folder, 'faqs_topic', None):
                    theme_id = IThemeCentreSchema(themecentre).tags
                    createFaqSmartFolder(faqs_folder, theme_id)

        # themecentre portlet smart folders should not rename themselves
        query = { 'portal_type': 'Topic',
                  'path': '/'.join(self.context.getPhysicalPath()) }
        brains = catalog.searchResults(query)
        for brain in brains:
            topic = brain.getObject()
            topic._at_rename_after_creation = False

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

class PromotionThemes(object):
    """ Old promotions might have themes as strings instead of lists. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = { 'portal_type': 'Promotion' }
        brains = catalog.searchResults(query)
        not_migrated = ''
        for brain in brains:
            obj = brain.getObject()
            if obj.schema['themes'].get(obj) == 'default':
                if IThemeTagging(obj).tags == ['d', 'e', 'f', 'a',
                                               'u', 'l', 't']:
                    IThemeTagging(obj).tags = ['default']
                else:
                    not_migrated += brain.getURL() + '\n'

        if not_migrated:
            return 'Some objects were not migrated\n' + not_migrated
        else:
            return 'success'

class ThemeLayoutAndDefaultPage(object):
    """ Removes the layout property on all themecentres and instead adds the
        default_page property with 'intro'. The intro document gets a layout
        property instead. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        query = {'object_provides': 'eea.themecentre.interfaces.IThemeCentre'}
        brains = self.context.portal_catalog.searchResults(query)
        for brain in brains:
            themecentre = brain.getObject()
            tc_base = aq_base(themecentre)
            intro = getattr(themecentre, 'intro', None)
            tc_layout = getattr(tc_base, 'layout', None)
            if intro:
                if tc_layout:
                    tc_base.__delattr__('layout')
                if not themecentre.hasProperty('default_page'):
                    themecentre.manage_addProperty('default_page', 'intro', 'string')
                if not intro.hasProperty('layout'):
                    intro.manage_addProperty('layout', 'themecentre_view', 'string')
                themecentre._p_changed = True
        return str(len(brains)) + ' themecentres migrated'

class GenericThemeToDefault(object):
    """ Migrates theme tags ['G','e','n','e','r','i','c'] or ['D', 'e', 'f', 'a', 'u', 'l', 't'] to ['default']. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query1 = { 'getThemes': 'G' }
        query2 = { 'getThemes': 'D' }
        query3 = { 'getThemes': 'g' }
        query4 = { 'getThemes': 'd' }
        queries = [query1,query2,query3,query4]
        output=''
        for query in queries:
           brains = catalog.searchResults(query)
           for brain in brains:
               if brain.getThemes == ['G', 'e', 'n', 'e', 'r', 'i', 'c'] or brain.getThemes == ['g', 'e', 'n', 'e', 'r', 'i', 'c'] or brain.getThemes == ['D', 'e', 'f', 'a', 'u', 'l', 't'] or brain.getThemes == ['d', 'e', 'f', 'a', 'u', 'l', 't']:
                  obj = brain.getObject()
                  themes = IThemeTagging(obj)
                  output=output+'NOTOK: '+obj.id+': '+'brain.getThemes[0]: '+ brain.getThemes[0] + ' themes.tags[0]: '+ (len(themes.tags) > 0 and themes.tags[0] or '') + ' URL: ' + obj.absolute_url() +'\r'
                  themes.tags = ['default']
                  obj.reindexObject()
               else:
                  output=output+'OK: '+brain.id+': '+'brain.getThemes[0]: '+ brain.getThemes[0] + 'URL:'+ brain.getURL() +'\r'
        return 'themes are migrated, RESULT:\r' + output

class EntriesWithThumbnail(object):
    """ Changes 'entries with thumbnail' to 10000 on all rss feed recipes
        in the rdf repository. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        repository = self.context
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'portal_type': 'RSSFeedRecipe',
                 'path': repository.getPhysicalPath() }
        brains = catalog.searchResults(query)
        for brain in brains:
            recipe = brain.getObject()
            recipe.setEntriesWithThumbnail(10000)
        return '%d rss recipes were migrated' % len(brains)

class ChangeDefaultPageToProperty(object):
    """ Changes default_page to being a property so it's visible in ZMI """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        query = {'object_provides': 'eea.themecentre.interfaces.IThemeCentre'}
        brains = self.context.portal_catalog.searchResults(query)
        for brain in brains:
            themecentre = brain.getObject()
            links = getattr(themecentre, 'links', None)
            news = getattr(themecentre, 'news', None)
            events = getattr(themecentre, 'events', None)

            for folder in filter(None, (links, news, events)):
                base = aq_base(folder)
                attr = getattr(base, 'default_page', None)
                has_property = base.hasProperty('default_page')
                # if object has a default_page attribute that is not a property
                if attr is not None and not has_property:
                    del base.default_page
                    base.manage_addProperty('default_page', attr, 'string')
        return "successfully migrated properties"

class EnsureAllObjectsHaveTags(object):
    """ Adds themecentre tag to all its objects if they don't have it
        already. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        themesdir = self.context
        portal_catalog = getToolByName(self.context, 'portal_catalog')

        count = 0
        path = '/'.join(themesdir.getPhysicalPath())
        brains = portal_catalog.searchResults(path=path)
        for brain in brains:
            if not brain.getThemes:
                obj = brain.getObject()
                themeCentre = getThemeCentre(obj)
                if themeCentre: 
                    themes = IThemeTagging(obj, None)
                    if themes:
                        themeCentreThemes = IThemeCentreSchema(themeCentre)
                        themes.tags = [themeCentreThemes.tags]
                        count += 1

        return str(count)  + " objects were tagged"

class ChangeMediaTypesDefault(object):
    """ Changes the media type on file's don't have any media type set.
        If media type not set, the type 'other' is set on the file. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(object_provides='p4a.video.interfaces.IVideoEnhanced')
        for brain in brains:
            file = brain.getObject()
            media = IMediaType(file)
            if not media.types:
                media.types = ['other']
            file.reindexObject()

        return "migration successful"

class AddRichTextDescriptionToVideos(object):
    """ Adds an empty string to the rich_description field on all
        IVideoEnhanced objects. As this is a new field it's None
        and the edit page fails with a traceback. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(object_provides='p4a.video.interfaces.IVideoEnhanced')
        for brain in brains:
            file = brain.getObject()
            video = IVideo(file)
            video.rich_description = u''
            video.urls = ()

        return str(len(brains)) + " videos where migrated."


class AddFolderAsLocallyAllowedTypeInLinks(object):
    """ Add the 'Folder' type as a locally addable type to all 'External link' folders in themecentres. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(object_provides=IThemeCentre.__identifier__)
        objs = [b.getObject() for b in brains]
        for obj in objs:
            linkfolder = None
            if 'links' in obj.objectIds():
                linkfolder = obj.links
            elif 'external-links' in obj.objectIds():
                linkfolder = obj['external-links']
    
            if linkfolder is not None:
                local = linkfolder.getLocallyAllowedTypes()
                immediate = linkfolder.getImmediatelyAddableTypes()
                if 'Folder' not in local:
                    linkfolder.setLocallyAllowedTypes(local + ('Folder',))
                if 'Folder' not in immediate:
                    linkfolder.setImmediatelyAddableTypes(immediate + ('Folder',))
    
        return 'successfully run'

class AddPressReleaseToHighlightsTopic(object):
    """ Adds PressRelease to the highlight topic's search criteria. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(object_provides=IThemeCentre.__identifier__)
        themecentres = [b.getObject() for b in brains]
        successful = 0
        
        for themecentre in themecentres:
            highlights_folder = getattr(themecentre, 'highlights')
            topic = getattr(highlights_folder, 'highlights_topic')
            crit = topic.getCriterion('Type_ATPortalTypeCriterion')
            value = crit.Value()
            if not 'Press Release' in value:
                crit.setValue(value + ('Press Release',))
            successful += 1

        return '%d highlight smart folders were modified' % successful
