""" Interfaces
"""
from zope.interface import Interface

class IRelatedPortlet(Interface):
    """ Related Portlet
    """

    def related():
        """ Return theme centres that are related to the current theme.
        """

class IRDFPortlet(Interface):
    """ RDF Portlet
    """

    def feeds():
        """ Returns the feeds that matches the current theme.
        """

class IRDFTitlesPortlet(Interface):
    """ RDF Titles Portlet
    """

    def feeds():
        """ Returns the feeds that matches the current theme.
        """

    def theme():
        """ Returns the theme of the current theme centre.
        """

class ILinksPortlet(Interface):
    """ Links Portlet
    """

    def published_link_items():
        """ Returns the links that match the current theme.
        """

class IFaqPortlet(Interface):
    """ Faq Portlet
    """

    def published_faq_items():
        """ Returns the faq objects that match the current theme.
        """

class IPortlet(Interface):
    """ Portlet
    """

    def all_link():
        """ All link
        """
        pass

    def short_items():
        """ Short items
        """
        pass

    def full_items():
        """ Full items
        """
        pass

    def title():
        """ Title
        """
        pass

class INewsPortlet(Interface):
    """ News Portlet
    """

    def short_items():
        """ Short items
        """
        pass

    def full_items():
        """ Full items
        """
        pass

class IEventsPortlet(Interface):
    """ EventsPortlet
    """
    def published_events():
        """ Published events
        """
        pass

    def full_items():
        """ Full items
        """
        pass

class IDCViewLogic(Interface):
    """ Marker interface DC ViewLogic
    """

    def folder_contents(size_limit):
        """ Folder contents """
