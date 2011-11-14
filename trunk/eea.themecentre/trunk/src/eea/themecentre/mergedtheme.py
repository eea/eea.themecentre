""" Merged theme
"""
from zope.interface import implements
from zope.component import adapts, getUtility
from eea.rdfrepository.interfaces import IRDFRepository
from eea.rdfrepository.utils import getFeedItemsWithoutDuplicates
from eea.themecentre.interfaces import IThemeTagging, IThemeTaggable
from eea.themecentre.interfaces import IMainThemeTagging
from zope.annotation.interfaces import IAnnotations
from zope.lifecycleevent import ObjectModifiedEvent, Attributes
from persistent.list import PersistentList
from zope.event import notify
from eea.themecentre.themetaggable import getMergedThemes
from eea.themecentre.themetaggable import ThemeTaggable, KEY, checkTheme

def getFeedsForSynonymousThemes(theme):
    """ There are for example reports_air and reports_acidification
        rdf feeds. When searching for 'air' feeds they will both
        show up. This method merges these into one and puts the feed
        items from both on the reports_air feed as that's the one
        actually being searched for.
    """
    category_feeds = { 'reports': [], 'indicators': [] }
    merged = []

    rdfrepository = getUtility(IRDFRepository)

    feeds = [feed for feed in rdfrepository.getFeeds(search={'theme': theme})
             if feed.id not in ('Atlas', 'datasets')]
    for feed in feeds:
        feed_id = feed.id
        theme_tag = IMainThemeTagging(feed.feed).tags

        if theme_tag == theme and feed_id.startsWith('reports_'):
            category_feeds['reports'].insert(feed)
        elif feed_id.startswith('reports_'):
            category_feeds['reports'].append(feed)
        elif theme_tag == theme and feed_id.startsWith('indicators_'):
            category_feeds['indicators'].insert(feed)
        elif feed_id.startswith('indicators_'):
            category_feeds['indicators'].append(feed)
        else:
            merged.append(feed)

    for category in ('indicators', 'reports'):
        if category_feeds[category]:
            items = []

            for feed in category_feeds[category]:
                items.extend(feed.items)
            items = getFeedItemsWithoutDuplicates(items, sort=True)

            # merge the items, all items are put on the feed that has
            # the argument 'theme' as its main theme
            category_feeds[category][0].items = items
            merged.insert(0, category_feeds[category][0])

    return merged

class ThemeTaggableMerged(ThemeTaggable):
    """ Theme Taggable Merged
    """
    implements(IThemeTagging)
    adapts(IThemeTaggable)

    def gett(self):
        """ Get tags
        """
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        tags = list(mapping['themes'])
        return getMergedThemes(self.context, tags)

    def sett(self, value):
        """ Set tags
        """
        # if the value didn't change we don't need to do anything
        if value == self.tags:
            return

        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)

        # if value is a tuple, convert it
        themes = list(value)
        # make sure object is tagged with the current themecentre
        # if not, add the themecentre to the tags
        checkTheme(self.context, themes)

        mapping['themes'] = PersistentList(themes)
        info = Attributes(IThemeTagging, 'tags')
        notify(ObjectModifiedEvent(self, info))

    tags = property(gett, sett)
