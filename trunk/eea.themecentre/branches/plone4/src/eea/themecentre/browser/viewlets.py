""" Viewlets
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class ThemesTagsViewlet(common.ViewletBase):
    """ A custom viewlet registered below the title for showing
        the tagged themes/topics
    """
    render = ViewPageTemplateFile('templates/themes_tags.pt')
