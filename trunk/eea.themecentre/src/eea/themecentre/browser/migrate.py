import urllib
from zope.interface import alsoProvides
from eea.themecentre.interfaces import IThemeCentreSchema, IThemeRelation, IThemeTagging
from eea.themecentre.browser.themecentre import PromoteThemeCentre
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.interfaces import INavigationRoot
import socket

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

class MigrateWrontThemeIds(object):
    """ migrate wrong theme ids to old correct """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context
        themeVocab = context.portal_vocabularies.themes         
        themeIds = themeVocab.objectIds()

        for theme in themeIds:
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
                obj.reindexObject()
                print '%s: %s -> %s' % (obj, currentThemes, newThemes) 

        for t in themeIds:
            newT = themeIdMap.get(t,t)
            if newT != t:
                obj = themeVocab[t]
                obj.setId(newT)
                obj.reindexObject()

class MigrateTheme(object):
    """ Migrate theme info from themes.eea.europa.eu zope 2.6.4 """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        newThemeId = self.context.getId()
        themeId = themeIdMap.get(newThemeId, newThemeId)
        try:
            self._title(themeId)
            self._intro(themeId)
            self._relatedThemes(themeId)
            self._links(themeId)
            self._image(themeId)
        except:
            print themeId + ' failed'
        
    def _title(self, themeId):
        titleUrl = url % ('themeTitle', themeId)
        title = urllib.urlopen(titleUrl).read()
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
            obj.reindexObject()

class InitialThemeCentres(object):
    """ create inital theme structure """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context

        fixThemeIds = MigrateWrontThemeIds(context, self.request)
        fixThemeIds()
        
        themeids = context.portal_vocabularies.themes.objectIds()[1:]
        noThemes = int(self.request.get('noThemes',0))
        if noThemes > 0:
            themeids = themeids[:noThemes]
        toMigrate = self.request.get('migrate', False)
        for theme in themeids:
            folder = context.invokeFactory('Folder', id=theme, title=theme)
            folder = context[folder]
            ptc = PromoteThemeCentre(folder, self.request)
            ptc()
            tc = IThemeCentreSchema(folder)
            tc.tags = theme
            

        if toMigrate:
            for theme in themeids:
                tc = context[theme]
                migrate = MigrateTheme(tc, self.request)
                migrate()

        if not hasattr(aq_base(context), 'right_slots'):
            context.manage_addProperty('right_slots', ['here/portlet_themes_related/macros/portlet',], type='lines')
        if not hasattr(aq_base(context), 'left_slots'):
            context.manage_addProperty('left_slots', ['here/portlet_navigation/macros/portlet',
                                                       'here/portlet_themes_rdftitles/macros/portlet'], type='lines')

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
            recipe.setFeedURL(feed_url)

            x = feed_url.find('theme=')
            if x > -1:
                theme = feed_url[x+6:].strip()
                taggable = IThemeTagging(recipe)
                taggable.tags = [theme]

            workflow.doActionFor(recipe, 'publish')


        return str(len(feeds)) + ' RDF/RSS files were successfully migrated.'
