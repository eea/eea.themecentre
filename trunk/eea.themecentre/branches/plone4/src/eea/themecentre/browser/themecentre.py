""" Browser themecentre module
"""
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import alsoProvides # implements
from zope.component import getUtility
from zope.formlib.form import Fields
from Products.Five.formlib.formbase import EditForm
from eea.themecentre.interfaces import IThemeCentre #I PossibleThemeCentre
from eea.themecentre.interfaces import IThemeCentreSchema, IThemeRelation
from eea.themecentre.themecentre import getTheme # PromotedToThemeCentreEvent
from eea.themecentre.themecentre import getThemeTitle
#TODO: fix me
#from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY
#TODO: fix me
#from eea.mediacentre.interfaces import IMediaCentre
#TODO: fix me
# - cleanup the below, is just to fix the imports
MEDIA_SEARCH_KEY = 'eea.mediacentre.search'
from zope.interface import Interface
class IMediaCentre(Interface):
    """ Dummy interface
    """

from eea.themecentre import _

ENABLE = 1 # Manual mode from ATContentTypes.lib.constraintypes

class PromoteThemeCentre(object):
    """ Promote a folder to a theme centre. """

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

        return self.request.RESPONSE.redirect(self.context.absolute_url() + '/themecentre_edit.html')

class ThemeCentreEdit(EditForm):
    """ Form for setting theme for a theme centre. """

    form_fields = Fields(IThemeCentreSchema, IThemeRelation)
    label = u'Promote theme centre'

class Multimedia(object):
    """ Provides multimedia information for a themecentre's multimedia section. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def types(self):
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
        currentTheme = getTheme(self.context)
        mediacentre = getUtility(IMediaCentre)
        search = { MEDIA_SEARCH_KEY: { 'theme': currentTheme }}
        return [mfile['object'] for mfile in mediacentre.getMedia(search=search)]

class Theme(object):
    """ Provides information about this theme/themecentre. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def name(self):
        return getThemeTitle(self.context)
