""" Viewlets
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter

class ThemesTagsViewlet(common.ViewletBase):
    """ A custom viewlet registered below the title for showing
        the tagged themes/topics
    """
    index = ViewPageTemplateFile('templates/themes_tags.pt')
    def available(self):
        """ Available
        """
        plone = getMultiAdapter((self.context, self.request),
                                name=u'plone_context_state')
        return plone.is_view_template()
