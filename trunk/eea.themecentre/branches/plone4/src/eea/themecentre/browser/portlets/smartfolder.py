""" Smart folder
"""
from Products.EEAContentTypes.browser import smartfolder
from eea.themecentre.themecentre import getThemeCentre
from eea.themecentre import _

class SmartFolderPortlets(smartfolder.SmartFolderPortlets):
    """ Smart Folder Portlets
    """

    def __call__(self):
        themecentre = getThemeCentre(self.context)
        if themecentre is None:
            return []
        else:
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
        else:
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
