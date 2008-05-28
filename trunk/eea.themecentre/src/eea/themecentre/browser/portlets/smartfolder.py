from Products.EEAContentTypes.browser import smartfolder
from eea.themecentre.themecentre import getThemeCentre

class SmartFolderPortlets(smartfolder.SmartFolderPortlets):

    def __call__(self):
        themecentre = getThemeCentre(self.context)
        if themecentre is None:
            return []
        else:
            return self.portlets(themecentre)

    def _sort_key(self, topic):
        id = topic.getId()

        if id == 'highlights_topic':
            return "1"
        elif id == 'events_topic':
            # we want events at the end
            return "zzz"
        else:
            # all topics don't need to be hardcoded, for the rest we
            # rely on the topic id for sorting
            return id

    def _title(self, topic):
        parent = topic.aq_parent
        parent_id = parent.getId()
        parent_title = parent.Title()

        if parent_id == 'events':
            title = 'Upcoming events'
        elif parent_id == 'faq':
            title = 'Latest FAQ'
        else:
            title = 'Latest ' + parent_title.lower()
        return title
