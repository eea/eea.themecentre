""" Sitemap
"""
from zope.interface import implements
from zope.component import adapts

from Products.CMFPlone.browser.navtree import (
    SitemapNavtreeStrategy,
    INavtreeStrategy
)

from eea.themecentre.interfaces import IThemeCentre

class SitemapThemeCentreStrategy(SitemapNavtreeStrategy):
    """ The navtree building strategy used by the sitemap, based on
       navtree_properties
    """
    implements(INavtreeStrategy)
    adapts(IThemeCentre)

    def __init__(self, context, view=None):
        SitemapNavtreeStrategy.__init__(self, context, view)
        self.rootPath = '/'.join(context.getPhysicalPath())
