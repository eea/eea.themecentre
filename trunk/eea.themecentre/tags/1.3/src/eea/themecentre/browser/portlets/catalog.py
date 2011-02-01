from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from eea.themecentre.themecentre import getThemeCentre, getTheme

class BasePortlet(utils.BrowserView):

    def short_items(self):
        items = self.items()
        result = []
        for item in items[:self.size]:
            result.append(self.item_to_short_dict(item))
        return result

    def full_items(self):
        items = self.items()
        result = []
        for item in items:
            result.append(self.item_to_full_dict(item))
        return result

    def all_link(self):
        context = utils.context(self)
        themeCentre = getThemeCentre(context)
        if themeCentre:
            # first let's see if view_name is in the request
            # if not we check the view_name class attribute
            view_name = getattr(self, 'view_name', None)
            if view_name:
                view_name = self.view_name
            if not view_name:
                view_name = self.request.get('view_name', None)
            if view_name:
                return themeCentre.absolute_url() + \
                       '/listall?view_name=' + view_name

        return ''

    def localized_time(self, time):
        context = utils.context(self)
        translation = getToolByName(context, 'translation_service')

        # sometimes time ends with a 'W'. That violates iso 8601, but
        # we take care of it anyway, pretend it's a 'Z'.
        if isinstance(time, (unicode, str)) and time.endswith('W'):
            time = time[:-1] + 'Z'

        localized_time = translation.ulocalized_time(time, None, context,
                domain='plone')
        return localized_time

    @property
    def size(self):
        return 3

class CatalogBasePortlet(BasePortlet):

    def items(self):
        context = utils.context(self)
        portal_catalog = getToolByName(context, 'portal_catalog')
        currentTheme = getTheme(context)

        if currentTheme:
            self.query['getThemes'] = currentTheme
            res = portal_catalog.searchResults(self.query)
        else:
            res = []

        return res

    def item_to_short_dict(self, item):
        return { 'title': item.Title,
                 'description': item.Description,
                 'url': item.getURL(),
                 'detail': self.localized_time(item.Date) }

    def item_to_full_dict(self, item):
        return { 'title': item.Title,
                 'description': item.Description,
                 'url': item.getURL(),
                 'body': item.Description,
                 'published': item.Date }
