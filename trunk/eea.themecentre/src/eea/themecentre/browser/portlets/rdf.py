from Products.CMFPlone import utils
from zope.component import getUtility
from zope.interface import implements

from eea.themecentre.themecentre import getTheme, getThemeCentre
from eea.themecentre.themecentre import RDF_THEME_KEY
from eea.themecentre.browser.interfaces import IRDFPortlet
from eea.rdfrepository.interfaces import IRDFRepository

from eea.themecentre.browser.portlets.catalog import BasePortlet

class RDFPortlet(BasePortlet):

    def short_items(self):
        context = utils.context(self)
        currentTheme = getTheme(context)
        themeCentre = getThemeCentre(context)
        result = []

        if currentTheme:
            rdfrepository = getUtility(IRDFRepository)
            search = { RDF_THEME_KEY: { 'theme': currentTheme }}
            feeds = rdfrepository.getFeedData(search)

            for feed in feeds:
                # temporary fix, "datasets" and "maps and graphs" feeds
                # should not be shown as portlets until they contain valid
                # dates
                if feed['id'] in ('datasets', 'Atlas'):
                    continue

                feed_match = []

                for entry in feed['items'][:self.size]:
                    # not all rdf feeds have date
                    if entry['date']:
                        detail = self.localized_time(entry['date'])
                    else:
                        # Those feeds that have no date should not be shown
                        continue

                    data = { 'title': entry['title'],
                             'url': entry['url'],
                             'image' : entry.get('image', None),
                             'detail': detail }
                    feed_match.append(data)

                if feed_match:
                    result.append({'title': feed['title'],
                                   'url': feed['url'],
                                   'detail': self.localized_time(feed['date']),
                                   'all_link': themeCentre.absolute_url() + \
                                       '/listfeed?feed=' + feed['id'],
                                   'items': feed_match })

        return result

    def full_items(self):
        context = utils.context(self)
        feed_id = self.request['feed']
        result = []

        currentTheme = getTheme(context)
        search = { RDF_THEME_KEY: { 'theme': currentTheme }}
        rdfrepository = getUtility(IRDFRepository)
        feed = rdfrepository.getFeedDataInFeed(feed_id, search)

        if len(feed) > 0:
            self.feedTitle = feed[0]['title']
            for item in feed[0]['items']:
                item['published'] = self.localized_time(item['date'])
                result.append(item)

        return result

    def title(self):
        return getattr(self, 'feedTitle', '')
