""" Browser themecentre module
"""
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import alsoProvides
from zope.component import getUtility
from zope.formlib.form import Fields
from five.formlib.formbase import EditForm
from eea.themecentre.interfaces import (
    IThemeCentreSchema,
    IThemeRelation,
    IThemeCentre
)
from eea.themecentre.themecentre import getTheme, getThemeTitle
from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY
from eea.mediacentre.interfaces import IMediaCentre
from eea.themecentre import _
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
ENABLE = 1 # Manual mode from ATContentTypes.lib.constraintypes

class PromoteThemeCentre(object):
    """ Promote a folder to a theme centre.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        alsoProvides(self.context, IThemeCentre)
        types = ['Folder', 'Document', 'Link', 'File', 'Image', 'Event',
                 'HelpCenterFAQFolder', 'FlashFile' ]

        self.context.setLocallyAllowedTypes( types + ['Topic'] )
        self.context.setImmediatelyAddableTypes( types )
        self.context.setConstrainTypesMode(ENABLE)

        return self.request.RESPONSE.redirect(
            self.context.absolute_url() + '/themecentre_edit.html')

class ThemeCentreEdit(EditForm):
    """ Form for setting theme for a theme centre.
    """

    form_fields = Fields(IThemeCentreSchema, IThemeRelation)
    label = u'Promote theme centre'

class Multimedia(object):
    """ Provides multimedia information for a themecentre's multimedia section.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def types(self):
        """ Types
        """
        #mediacentre = getUtility(IMediaCentre)
        #types = sorted(mediacentre.getMediaTypes())
        vocab = getUtility(IVocabularyFactory, name="Media types")(self.context)
        # we have titles of single name so we add 's' and since we know it's in
        # english
        types_ = [{'typeid':term.value, 'title':_(term.title+'s')}
                  for term in vocab if term.value != 'other']
        types_.append({'typeid':'other', 'title': _(u'Other')})
        return types_

    def media_items(self):
        """ Media items
        """
        currentTheme = getTheme(self.context)
        mediacentre = getUtility(IMediaCentre)
        search = { MEDIA_SEARCH_KEY: { 'theme': currentTheme }}
        return [mfile['object']
                    for mfile in mediacentre.getMedia(search=search)]

class Theme(object):
    """ Provides information about this theme/themecentre.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def name(self):
        """ Name
        """
        return getThemeTitle(self.context)

class ThemecentreUtils(BrowserView):
    """ Themecentre catalog search and utils methods """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.catalog = getToolByName(context, 'portal_catalog')
        self.now = DateTime()

    def getSubtopics(self):
        """ get sub objects from current theme object
        that are assigned to nav section topics, this is
        regarded as the subtopics of the theme. Return list sorted on title."""
        folder_path = '/'.join(self.context.getPhysicalPath())
        query = {
                'navSection' : 'topics',
                'review_state'       : 'published',
                'sort_on'            : 'sortable_title',
                'path'               : {'query': folder_path, 'depth': 1},
                'effectiveRange'     : self.now
        }
        res = self.catalog.searchResults(query)
        return res

    def getDataCentreName(self):
        """ Get the name of the datacentre for the given theme
            of the context
        """
        name = ''
        name = getThemeTitle(self.context)
        if name:
            return name.capitalize()
        else:
            name = getThemeTitle(self.context.aq_inner.aq_parent)
            name = [name.capitalize() if name else ''].pop()
            return name

