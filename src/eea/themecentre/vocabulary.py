""" Vocabulary
"""
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName


class ThemesVocabulary(object):
    """ Themes Vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context, checkContext=True):
        site = getSite()
        portal_vocab = getToolByName(site, 'portal_vocabularies')
        themes = getattr(portal_vocab, 'themes').getDisplayList(site)
        terms = [SimpleTerm(key, key, value) for key, value in themes.items()]
        return SimpleVocabulary(terms)


ThemesVocabularyFactory = ThemesVocabulary()


class ThemesEditVocabulary(object):
    """ Theme vocabulary that is used for the 'themes' tab. This vocabulary
        has knowledge about deprecated themes.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        portal_vocab = getToolByName(site, 'portal_vocabularies')
        wftool = getToolByName(site, 'portal_workflow')

        themes = portal_vocab.themes.objectValues()
        terms = []
        for theme in themes:
            key = theme.getId()
            state = wftool.getInfoFor(theme, 'review_state', 'published')
            if state == 'published':
                terms.append(SimpleTerm(key, key, theme.Title()))
        return SimpleVocabulary(terms)


ThemesEditVocabularyFactory = ThemesEditVocabulary()


class ThemeCentresVocabulary(object):
    """ Theme Centres Vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, themeCentreAdapted):
        theme_centre = themeCentreAdapted.context
        catalog = getToolByName(theme_centre, 'portal_catalog')
        iface = 'eea.themecentre.interfaces.IThemeCentre'
        res = catalog.searchResults({'Language': 'en',
                                     'object_provides': iface})
        terms = []
        for brain in res:
            obj = brain.getObject()
            uid = obj.UID()
            # add the theme centre to vocabulary if it's not the current theme
            if uid != theme_centre.UID():
                terms.append(SimpleTerm(uid, uid, brain.Title))
        return SimpleVocabulary(terms)


ThemeCentresVocabularyFactory = ThemeCentresVocabulary()

vocabs = {
    'popular-searches': (
        ('air-quality', 'Air quality'),
        ('greenhouse-gases', 'Greenhouse gases'),
        ('carbon-farming', 'Carbon farming'),
        ('bathing-water', 'Bathing water'),
        ('loss-biodiversity', 'Loss of biodiversity'),
        ('environmental-policy-instruments',
            'Environmental policy instruments'),
        ('waste-management', 'Waste management'),
        ('renewable-energy', 'Renewable energy'),
        ('carbon-footprint', 'Carbon footprint'),
        ('water-stress', 'Water stress'),
        ('particulate-matter', 'Particulate matter'),
        ('lrtap', 'Lrtap'),
        ('wei', 'Wei')
    )
}
