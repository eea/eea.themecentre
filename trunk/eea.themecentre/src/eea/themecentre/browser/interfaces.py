from zope.interface import Interface

class IRelatedPortlet(Interface):

    def related():
        """ Return theme centres that are related to the current theme. """
