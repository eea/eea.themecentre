""" Vocabulary
"""
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

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
        themeCentre = themeCentreAdapted.context
        catalog = getToolByName(themeCentre, 'portal_catalog')
        iface = 'eea.themecentre.interfaces.IThemeCentre'
        res = catalog.searchResults({ 'Language' : 'en',
                                      'object_provides' : iface })
        terms = []
        for brain in res:
            obj = brain.getObject()
            uid = obj.UID()
            # add the theme centre to vocabulary if it's not the current theme
            if uid != themeCentre.UID():
                terms.append(SimpleTerm(uid, uid, brain.Title))
        return SimpleVocabulary(terms)

ThemeCentresVocabularyFactory = ThemeCentresVocabulary()
