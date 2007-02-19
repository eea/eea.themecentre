from zope.interface import Interface
from zope.schema import List, TextLine, Choice
from zope.schema.vocabulary import SimpleVocabulary
#from eea.themecentre.vocabulary import getThemesVocab

class IThemeTaggable(Interface):
    """ Marker interface for content objects that can be tagged. """

class IThemeTagging(Interface):

    tags = List(
        title = u"Themes",
        description = u"List of themes that this content object should be "
                       "associated with",
        required = False,
        value_type = Choice(
            title = u"Theme",
            vocabulary = "Allowed themes",
            )
        )

    def addTag(self, theme):
        """ Adds 'theme' tag to the content object. """
