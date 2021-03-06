""" Smart folder
"""
from eea.themecentre.themecentre import getThemeCentre
from eea.themecentre import eeaMessageFactory as _
try:
    from Products.EEAContentTypes.browser import smartfolder
    SFP = smartfolder.SmartFolderPortlets
except (ImportError, AttributeError):
    from Products.Five.browser import BrowserView

    class SFP(BrowserView):
        """ Smart Folder Portlets """


class SmartFolderPortlets(SFP):
    """ Smart Folder Portlets
    """

    def __call__(self):
        themecentre = getThemeCentre(self.context)
        if themecentre is None:
            return []
        return self.portlets(themecentre)

    def _sort_key(self, topic):
        """ Sort key of topic
        """
        tid = topic.getId()

        if tid == 'highlights_topic':
            return "1"
        elif tid == 'events_topic':
            # we want events at the end
            return "zzz"
        # all topics don't need to be hardcoded, for the rest we
        # rely on the topic id for sorting
        return tid

    def _title(self, topic):
        """ Returns harcoded titles if matched criteria otherwise default title
        """
        obj = self._parent_or_topic(topic)
        obj_id = obj.getId()
        obj_title = obj.Title()

        if obj_id == 'events':
            title = _(u'Upcoming events')
        elif obj_id == 'faq':
            title = _(u'Latest FAQ')
        else:
            title = obj_title
        return title
