from zope.interface import Interface

class IRelatedPortlet(Interface):

    def related():
        """ Return theme centres that are related to the current theme. """

class IRDFPortlet(Interface):

    def feeds():
        """ Returns the feeds that matches the current theme. """

class IRDFTitlesPortlet(Interface):

    def feeds():
        """ Returns the feeds that matches the current theme. """

    def theme():
        """ Returns the theme of the current theme centre. """

class ILinksPortlet(Interface):

    def published_link_items():
        """ Returns the links that match the current theme. """

class IFaqPortlet(Interface):

    def published_faq_items():
        """ Returns the faq objects that match the current theme. """

class IPortlet(Interface):

    def all_link():
        pass

    def short_items():
        pass

    def full_items():
        pass

    def title():
        pass
    
class INewsPortlet(Interface):

    def short_items():
        pass

    def full_items():
        pass

class IEventsPortlet(Interface):
    def published_events():
        pass

    def full_items():
        pass
