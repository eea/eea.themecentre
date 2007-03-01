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
        max_length = 3,
        value_type = Choice(
            title = u"Theme",
            vocabulary = "Allowed themes",
            )
        )

    def addTag(self, theme):
        """ Adds 'theme' tag to the content object. """


class IPossibleThemeCentre(Interface):
    """ Marker interface for objects that can become a theme centre. """

class IThemeCentre(Interface):
    """ Marker interface for objects that are promoted to a theme centre. """
    
    def getReports():
        """ return a list of reports for this theme centre. """

    def getHighlights():
        """ return a list of highlits for this theme centre. """

    def getArticles():
        """ return a list of articles for this theme centre. """

    def getIndicators():
        """ return a list of indicators for this theme centre. """

    def getData():
        """ return a list of data from data service for this theme centre. """

    def getVideos():
        """ return a list of videos for this theme centre. """

    
class IThemeCentreSchema(Interface):
    """ Theme centre schema for the edit form. """
    
    tags = Choice(
            title = u"Theme",
            description = u"Theme that this object should be centre for",
            required = True,            
            vocabulary = "Allowed themes",
        )


class IThemeRelation(Interface):
    """ A theme can be related to other themes. """

    related = List(
        title = u"Related themes",
        description = u"List of themes that this theme is related to.",
        required = False,
        max_length = 5,
        value_type = Choice(
            title = u"Theme",
            vocabulary = "Theme Centres",
            )
        )
