""" Merged theme
"""
from zope.interface import implements
from zope.component import adapts
from eea.themecentre.interfaces import IThemeTagging, IThemeTaggable
from zope.annotation.interfaces import IAnnotations
from zope.lifecycleevent import ObjectModifiedEvent, Attributes
from persistent.list import PersistentList
from zope.event import notify
from eea.themecentre.themetaggable import getMergedThemes
from eea.themecentre.themetaggable import ThemeTaggable, KEY, checkTheme


class ThemeTaggableMerged(ThemeTaggable):
    """ Theme Taggable Merged
    """
    implements(IThemeTagging)
    adapts(IThemeTaggable)

    def gett(self):
        """ Get tags
        """
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        tags = list(mapping['themes'])
        return getMergedThemes(self.context, tags)

    def sett(self, value):
        """ Set tags
        """
        # if the value didn't change we don't need to do anything
        if value == self.tags:
            return

        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)

        # if value is a tuple, convert it
        themes = list(value)
        # make sure object is tagged with the current themecentre
        # if not, add the themecentre to the tags
        checkTheme(self.context, themes)

        mapping['themes'] = PersistentList(themes)
        info = Attributes(IThemeTagging, 'tags')
        notify(ObjectModifiedEvent(self, info))

    tags = property(gett, sett)
