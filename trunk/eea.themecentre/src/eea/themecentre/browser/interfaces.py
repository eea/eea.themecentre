from zope.interface import Interface

class IRelatedPortlet(Interface):

    def related():
        """ Return theme centres that are related to the current theme. """

class IRDFPortlet(Interface):

    def feeds():
        """ Returns the feeds that matches the current theme. """
