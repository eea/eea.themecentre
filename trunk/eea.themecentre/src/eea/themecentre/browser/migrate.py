import urllib
from eea.themecentre.interfaces import IThemeRelation
from eea.themecentre.browser.themecentre import PromoteThemeCentre

url = 'http://themes.eea.europa.eu/migrate/%s?theme=%s'

class MigrateTheme(object):
    """ Migrate theme info from themes.eea.europa.eu zope 2.6.4 """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        themeId = self.context.getId()
        self._title(themeId)
        self._intro(themeId)
        self._relatedThemes(themeId)

    def _title(self, themeId):
        titleUrl = url % ('themeTitle', themeId)
        title = urllib.urlopen(titleUrl).read()
        self.context.setTitle(title)

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
            obj.setText(introText)

    def _links(self, themeId):
        import pdb; pdb.set_trace()
        linksUrl = url % ('themeLinks', themeId)
        links = urllib.urlopen(linksUrl).read().strip()
        links = links.split('\n')
        folder = self.context.links
        for link in links:
            link = link.split(';')
            linkId = folder.invokeFactory('Link', id=link[0].strip())
            obj = linkfolder[linkId]
            obj.setTitle(link[1].strip())
            obj.setRemoteUrl(link[2].strip())
            

class InitialThemeCentres(object):
    """ create inital theme structure """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context
        themeids = self.context.portal_vocabularies.themes.objectIds()
        for theme in themeids:
            tc = context.invokeFactory('Folder', id=theme)
            tc = context[tc]
            ptc = PromoteThemeCentre(tc, self.request)
            ptc()
