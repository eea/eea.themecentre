from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from Products.CMFCore.utils import getToolByName

class ThemesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_vocab = getToolByName(context.context, 'portal_vocabularies')
        themes = getattr(portal_vocab,
                'themes').getDisplayList(context.context)
        terms = [SimpleTerm(key, key, value) for key, value in themes.items()]
        return SimpleVocabulary(terms)

ThemesVocabularyFactory = ThemesVocabulary()

class ThemesEditVocabulary(object):
    """ Theme vocabulary that is used for the 'themes' tab. This vocabulary
        has knowledge about deprecated themes. """
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_vocab = getToolByName(context.context, 'portal_vocabularies')
        wftool = getToolByName(context.context, 'portal_workflow')

        themes = portal_vocab.themes.objectValues()
        terms = []
        for theme in themes:
            key = theme.getId()
            state = wftool.getInfoFor(theme, 'review_state', 'published')
            if state != 'published':
                title = theme.Title() + ' (deprecated)'
            else:
                title = theme.Title()
            terms.append(SimpleTerm(key, key, title))
        return SimpleVocabulary(terms)

ThemesEditVocabularyFactory = ThemesEditVocabulary()

class ThemeCentresVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, themeCentreAdapted):
        themeCentre = themeCentreAdapted.context
        catalog = getToolByName(themeCentre, 'portal_catalog')
        iface = 'eea.themecentre.interfaces.IThemeCentre'
        res = catalog.searchResults(object_provides=iface)
        terms = []
        for brain in res:
            obj = brain.getObject()
            uid = obj.UID()
            # add the theme centre to vocabulary if it's not the current theme
            if uid != themeCentre.UID():
                terms.append(SimpleTerm(uid, uid, brain.Title))
        return SimpleVocabulary(terms)

ThemeCentresVocabularyFactory = ThemeCentresVocabulary()
