from zope.interface import Interface

class IRelatedPortlet(Interface):

    def related():  #pylint: disable-msg = E0211
        """ Return theme centres that are related to the current theme. """

class IRDFPortlet(Interface):

    def feeds():  #pylint: disable-msg = E0211
        """ Returns the feeds that matches the current theme. """

class IRDFTitlesPortlet(Interface):

    def feeds():  #pylint: disable-msg = E0211
        """ Returns the feeds that matches the current theme. """

    def theme():  #pylint: disable-msg = E0211
        """ Returns the theme of the current theme centre. """

class ILinksPortlet(Interface):

    def published_link_items():  #pylint: disable-msg = E0211
        """ Returns the links that match the current theme. """

class IFaqPortlet(Interface):

    def published_faq_items():  #pylint: disable-msg = E0211
        """ Returns the faq objects that match the current theme. """

class IPortlet(Interface):

    def all_link():  #pylint: disable-msg = E0211
        pass

    def short_items():  #pylint: disable-msg = E0211
        pass

    def full_items():  #pylint: disable-msg = E0211
        pass

    def title():  #pylint: disable-msg = E0211
        pass
    
class INewsPortlet(Interface):

    def short_items():  #pylint: disable-msg = E0211
        pass

    def full_items():  #pylint: disable-msg = E0211
        pass

class IEventsPortlet(Interface):
    def published_events():  #pylint: disable-msg = E0211
        pass

    def full_items():  #pylint: disable-msg = E0211
        pass

class IDCViewLogic(Interface):
    """Marker interface
    """

    def folder_contents(size_limit):  #pylint: disable-msg = E0213
        """ """
