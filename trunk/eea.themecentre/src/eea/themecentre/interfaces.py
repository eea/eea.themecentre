from zope.interface import Interface

class IThemeTaggable(Interface):
    """ Marker interface for content objects that can be tagged. """

class IThemeTagging(Interface):
    def addTag(self, theme):
        """ Add 'theme' tag to the content object. """

    def tags():
        """ Returns all theme tags this object has. """
