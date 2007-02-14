from eea.themecentre.interfaces import IThemeTagging
from eea.themecentre.interfaces import IThemeTaggable
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.app.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.event import notify
from zope.interface import implements
from zope.app.event.objectevent import ObjectModifiedEvent, Attributes

KEY = 'eea.themecentre.themetaggable'

class ThemeTaggable(object):
    implements(IThemeTagging)
    adapts(IThemeTaggable)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            themes =  { 'themes': PersistentList() }
            mapping = annotations[KEY] = PersistentDict(themes)
        self.mapping = mapping

    def addTag(self, theme):
        existing_themes = self.mapping['themes']
        existing_themes.append(theme)

        info = Attributes(IThemeTaggable, 'tags')
        notify(ObjectModifiedEvent(self.context, info))

    @property
    def tags(self):
        return self.mapping['themes']
