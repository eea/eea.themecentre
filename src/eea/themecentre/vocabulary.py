""" Vocabulary
"""
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.component.hooks import getSite
from zope.component import getUtility, queryUtility
from Products.CMFCore.utils import getToolByName
from collective.taxonomy.interfaces import ITaxonomy


utility_name = "collective.taxonomy.themes"


class ThemesVocabulary(object):
    """ Themes Vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context, checkContext=True):
        taxonomy = queryUtility(ITaxonomy, name=utility_name)

        try:
            vocabulary = taxonomy(self)
        except:
            vocabulary = taxonomy.makeVocabulary('en')

        terms = [
            SimpleTerm(key, key, val.encode('ascii', 'ignore').decode('ascii'))
            for val, key in vocabulary.iterEntries()
        ]

        return SimpleVocabulary(terms)


ThemesVocabularyFactory = ThemesVocabulary()


class ThemesEditVocabulary(object):
    """ Theme vocabulary that is used for the 'themes' tab. This vocabulary
        has knowledge about deprecated themes.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        taxonomy = queryUtility(ITaxonomy, name=utility_name)

        try:
            vocabulary = taxonomy(self)
        except:
            vocabulary = taxonomy.makeVocabulary('en')

        terms = [
            SimpleTerm(key, key, val.encode('ascii', 'ignore').decode('ascii'))
            for val, key in vocabulary.iterEntries()
        ]

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
