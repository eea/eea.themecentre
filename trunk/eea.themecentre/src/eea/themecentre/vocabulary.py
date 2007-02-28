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
