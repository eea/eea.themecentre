""" Interfaces """
from zope.interface import Interface, Attribute
from zope.schema import List, Choice


class IThemeTaggable(Interface):
    """ Marker interface for content objects that can be tagged. """

class IThemeTagging(Interface):
    """ Theme tagging """

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

class IMainThemeTagging(IThemeTagging):
    """ Works like IThemeTagging, but only returns the main theme. """

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

class IThemeCentreListFeed(Interface):
    """ Each item in themecentre full feed list provides this interface. """

    title = Attribute("feed item title")
    url = Attribute("feed item link")
    summary = Attribute("feed item summary")
    published = Attribute("feed item detail")

class IThemeMoreLink(Interface):
    """ Refers to a more link. """

    url = Attribute("more link")

class IThemeCentreImageUrl(Interface):
    """ Returns the url to the image in the canonical theme centre. """
