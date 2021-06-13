""" Browser themecentre module
"""
from DateTime import DateTime

from zope.schema.interfaces import IVocabularyFactory
from zope.interface import alsoProvides, Interface
from zope.component import queryUtility, getUtility
from zope.formlib.form import Fields
from five.formlib.formbase import EditForm
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from eea.themecentre.interfaces import IThemeCentreSchema
from eea.themecentre.interfaces import IThemeRelation
from eea.themecentre.interfaces import IThemeCentre
from eea.themecentre.themecentre import getTheme, getThemeTitle
from eea.themecentre import eeaMessageFactory as _
try:
    from eea.mediacentre.mediacentre import MEDIA_SEARCH_KEY
    from eea.mediacentre.interfaces import IMediaCentre
except ImportError:
    MEDIA_SEARCH_KEY = "eea.mediacentre.search"

    class IMediaCentre(Interface):
        """ IMediaCentre """
try:
    from eea.promotion.interfaces import IPromotion
except ImportError:
    class IPromotion(Interface):
        """ IPromotion """

ENABLE = 1  # Manual mode from ATContentTypes.lib.constraintypes


class PromoteThemeCentre(object):
    """ Promote a folder to a theme centre.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        alsoProvides(self.context, IThemeCentre)
        types = ['Folder', 'Document', 'Link', 'File', 'Image', 'Event',
                 'FlashFile']

        self.context.setLocallyAllowedTypes(types + ['Topic'])
        self.context.setImmediatelyAddableTypes(types)
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
        vocab = queryUtility(IVocabularyFactory, name="Media types")
        vocab = vocab(self.context)
        # we have titles of single name so we add 's' and since we know it's in
        # english
        types_ = [{'typeid': term.value, 'title': _(term.title + 's')}
                  for term in vocab if term.value != 'other']
        types_.append({'typeid': 'other', 'title': _(u'Other')})
        return types_

    def media_items(self):
        """ Media items
        """
        currenttheme = getTheme(self.context)
        mcentre = queryUtility(IMediaCentre)
        if not mcentre:
            return []
        search = {MEDIA_SEARCH_KEY: {'theme': currenttheme}}
        return [mfile['object']
                for mfile in mcentre.getMedia(search=search)]


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

    def getSubtopics(self, path=None):
        """ get sub objects from current theme object
        that are assigned to nav section topics, this is
        regarded as the subtopics of the theme. Return list sorted on title."""
        folder_path = '/'.join(self.context.getPhysicalPath())
        folder_path = path if path else folder_path
        query = {
            'navSection': 'topics',
            'review_state': 'published',
            'sort_on': 'sortable_title',
            'path': {'query': folder_path, 'depth': 1},
            'effectiveRange': self.now
        }

        if path:
            del query['navSection']
            query['portal_type'] = ('Topic', 'Collection')
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
        name = getThemeTitle(self.context.aq_inner.aq_parent)
        name = [name.capitalize() if name else ''].pop()
        return name

    def getPromotedItem(self, ptype=None, itype=None):
        """ get promoted item
        """
        query = {
            'object_provides': {
                'query': [
                    'eea.promotion.interfaces.IPromoted'
                ],
            },
            'review_state': 'published',
            'sort_on': 'effective',
            'sort_order': 'reverse',
        }
        if itype:
            query['object_provides']['operator'] = 'and'
            query['object_provides']['query'].append(itype)
        if ptype:
            query['portal_type'] = ptype

        context = self.context.aq_inner
        query['getThemes'] = getTheme(context)
        catalog = getToolByName(context, 'portal_catalog')
        result = catalog(query)
        item = None
        for brain in result:
            item = brain.getObject()
            promo = IPromotion(item)
            if not promo.display_on_themepage:
                continue
            if not promo.active:
                continue
            break
        return item

    def getThemeName(self):
        """ Get theme name of the context to construct the url to the
            themecentre and the datacentre page
        """
        return getTheme(self.context.aq_inner)

    def getLatestStorytelling(self):
        """ Get Latest Storytelling items for themecentre
        """
        return self.context.getFolderContents(contentFilter={
                            'portal_type': 'Storytelling'}, full_objects=True)

    def getLatestIndicators(self):
        """ Get Latest indicators items for themecentre
        """
        data_maps = self.context.restrictedTraverse("data_and_maps_logic")
        return data_maps.getLatestIndicators()

    def getLatestNews(self):
        """ Get Latest news items for themecentre
        """
        frontpage = self.context.restrictedTraverse("frontpage_highlights")
        return frontpage.getLatest("newsandarticles",
                                   products_category='getThemecentreProducts')

    def getLatestPublications(self):
        """ Get Latest publications items for themecentre
        """
        frontpage = self.context.restrictedTraverse("frontpage_highlights")
        frontpage.noOfLow = 2
        return frontpage.searchResults("publications", searchtype='Report')

    def getPromotedGISMap(self):
        """ Get Latest promoted GIS Maps items for themecentre
        """
        return self.getPromotedItem(ptype="GIS Application")


    def getPromotedMultimedia(self):
        """ Get Latest promoted multimedia item for themecentre
        """
        return self.getPromotedItem(itype="eea.mediacentre.interfaces.IVideo")

    def getPromotedTableauDashboard(self):
        """ Get Latest promoted Tableau Dashboard item for themecentre
        """
        return self.getPromotedItem(ptype="Dashboard")

    def is_expired_or_unpublished(self, pid):
        """
        :param pid:  object id to check if object is expired or unpublished
        :return: boolean
        """
        obj = self.context.restrictedTraverse(pid, None)
        if not obj:
            return True
        wftool = getToolByName(obj, 'portal_workflow')
        review_state = wftool.getInfoFor(obj, 'review_state')
        if review_state != 'published':
            return True
        if obj.restrictedTraverse('@@plone_interface_info').provides(
                'eea.workflow.interfaces.IObjectArchived'):
            return True
        return False

    def get_vocabulary_lines(self):
        """ Imitate vocabulary.getVocabularyLines using taxonomy
        """
        vocab = getUtility(IVocabularyFactory, 'Allowed themes')
        terms = vocab(self)

        themes = []
        for term in terms:
            themes.append((term.value, term.title))

        return themes