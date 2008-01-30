from zope.interface import Interface, Attribute
from zope.schema import List, TextLine, Choice
from zope.schema.vocabulary import SimpleVocabulary
from Products.EEAContentTypes.interfaces import IFeedPortletInfo


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

class IThemeCentrePortletInfo(IFeedPortletInfo):
    """ Any object that wants to be displayed in a themecentre portlet
        should provide an adapter providing this interface. """

class IThemeCentrePortletItem(Interface):
    """ Each item in the themecentre portlets provides this interface. """

    title = Attribute("portlet item title")
    url = Attribute("portlet item link")
    detail = Attribute("portlet item detail")
    image = Attribute("portlet item image")

class IThemeCentreListFeed(Interface):
    """ Each item in themecentre full feed list provides this interface. """

    title = Attribute("feed item title")
    url = Attribute("feed item link")
    summary = Attribute("feed item summary")
    published = Attribute("feed item detail")
