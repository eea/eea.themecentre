from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements, alsoProvides
from zope.component import getUtility
from zope.formlib.form import Fields
from Products.Five.formlib.formbase import EditForm
from eea.themecentre.interfaces import IThemeCentre, IPossibleThemeCentre
from eea.themecentre.interfaces import IThemeCentreSchema, IThemeRelation
from eea.themecentre.themecentre import PromotedToThemeCentreEvent, getTheme
from eea.themecentre.themecentre import getThemeTitle
from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY
from eea.mediacentre.mediatypes import MediaTypesVocabularyFactory
from eea.mediacentre.interfaces import IMediaCentre
from Products.CMFCore.utils import getToolByName

ENABLE = 1 # Manual mode from ATContentTypes.lib.constraintypes

class PromoteThemeCentre(object):
    """ Promote a folder to a theme centre. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        alsoProvides(self.context, IThemeCentre)
        types = [ 'Folder', 'Document', 'Link', 'File', 'Image', 'Event',
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
        mediacentre = getUtility(IMediaCentre)
        types = sorted(mediacentre.getMediaTypes())
        vocab = getUtility(IVocabularyFactory, name="Media types")(self.context)
        types_ = [{'url':'theme'+term.value, 'title':term.title}
                  for term in vocab if term.value != 'other']
        types_.append({'url': 'themeother', 'title': 'Other'})
        return types_

    def media_items(self):
        currentTheme = getTheme(self.context)
        mediacentre = getUtility(IMediaCentre)
        search = { MEDIA_SEARCH_KEY: { 'theme': currentTheme }}
        return [file['object'] for file in mediacentre.getMedia(search=search)]

class Theme(object):
    """ Provides information about this theme/themecentre. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def name(self):
        return getThemeTitle(self.context)
