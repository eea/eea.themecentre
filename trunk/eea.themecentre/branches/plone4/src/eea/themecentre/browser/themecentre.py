""" Browser themecentre module
"""
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import alsoProvides
from zope.component import getUtility
from zope.formlib.form import Fields
from Products.Five.formlib.formbase import EditForm
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

        self.context.setLocallyAllowedTypes( types + ['RichTopic', 'Topic'] )
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

    def getThemeFolders(self):
        """ get folders from current theme object """
        folder_path = '/'.join(self.context.aq_parent.getPhysicalPath())
        query = {
                'portal_type'        : 'Folder',
                'review_state'       : 'published',
                'sort_on'            : 'effective',
                'exclude_from_nav'   : False,
                'sort_order'         : 'reverse',
                'path'               : {'query': folder_path, 'depth': 1},
                'effectiveRange'     : self.now
        }
        return self.catalog.searchResults(query)

    def getDataCentreName(self):
        """ Get the name of the datacentre for the given theme
            of the context
        """
        name = ''
        name = getTheme(self.context)
        if name:
            return name.capitalize()
        else:
            name = getTheme(self.context.aq_inner.aq_parent)
            name = [name.capitalize() if name else ''].pop()
            return name

    def migrateThemeFolders(self):
        """ Removes the intro page as the default_page and sets
            the layout of theme folders to themecentre_view and
            sets as description for the folder the description
            of the intro page if exists, otherwise it constucts
            one from the first paragraph
        """
        query = { 'object_provides' :
                'eea.themecentre.interfaces.IThemeCentre',
                'review_state': 'published', 'path' :
                {'query': '/www/SITE/themes', 'depth': 1}}
        res = self.catalog.searchResults(query)
        res = [obj.getObject() for obj in res]
        for obj in res:
            if hasattr(obj, 'intro'):
                intro = obj.intro
            else:
                intro = obj.restrictedTraverse(obj.getProperty('default_page'))
            if obj.hasProperty('layout'):
                obj.manage_changeProperties({'layout' : 'themecentre_view'})
            else:
                obj.manage_addProperty('layout', 'themecentre_view', 'string')
            if obj.hasProperty('default_page'):
                obj.manage_delProperties(['default_page'])
            if intro.hasProperty('layout'):
                obj.manage_delProperties(['layout'])
            intro_desc = intro.Description()
            if intro_desc:
                obj.setDescription(intro_desc)
            else:
                import lxml.html
                body = lxml.html.fromstring(intro.CookedBody())
                if len(body.findall('p')) > 0:
                    first_paragraph = body.findall('p')[0].text
                else:
                    first_paragraph = body.text
                obj.setDescription(first_paragraph)
        return "done"



