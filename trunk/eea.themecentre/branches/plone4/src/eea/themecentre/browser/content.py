""" Content
"""
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

from eea.themecentre.interfaces import IThemeCentreSchema

class ContentByType(object):
    """ Provides data to the contentbytheme template that shows a list
        of all content objects with certain portal type and certain
        theme tags.
    """

    def __init__(self, context, request):
        b_start = request.get('b_start', 0)
        contenttype = request.get('contenttype', None)

        self.title = context.Title()
        self.description = ''

        if contenttype is None:
            self.batch = Batch([], 30, int(b_start), orphan=0)
            return

        themes = IThemeCentreSchema(context).tags

        catalog = getToolByName(context, 'portal_catalog')
        query = { 'portal_type': contenttype,
                  'review_state': 'published',
                  'sort_on': 'effective',
                }
        if themes:
            query['getThemes'] = themes
        contentobjects = []
        brains = catalog.searchResults(query)
        for brain in brains:
            obj = { 'title': brain.Title,
                    'description': brain.Description,
                    'url': brain.getURL(),
                    'url_title': brain.Title,
                  }
            contentobjects.append(obj)

        self.content = contentobjects
        self.batch = Batch(self.content, 30, int(b_start), orphan=0)
