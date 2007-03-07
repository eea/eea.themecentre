from eea.themecentre.interfaces import IThemeTagging, IThemeTaggable
from eea.themecentre.interfaces import IThemeCentre
from eea.themecentre.interfaces import IThemeCentreSchema
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.app.annotation.interfaces import IAnnotations
from zope.component import adapts, getUtility
from zope.event import notify
from zope.interface import implements
from zope.app.event.objectevent import ObjectModifiedEvent, Attributes
from zope.app.schema.vocabulary import IVocabularyFactory

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

    def tags():
        def get(self):
            anno = IAnnotations(self.context)
            mapping = anno.get(KEY)
            return list(mapping['themes'])
        def set(self, value):
            anno = IAnnotations(self.context)
            mapping = anno.get(KEY)
            mapping['themes'] = PersistentList(value)
            self.context.reindexObject()
        return property(get, set)
    tags = tags()

class ThemeCentreTaggable(object):
    implements(IThemeCentreSchema)
    adapts(IThemeCentre)

    def __init__(self, context):
        self.context = context

    def tags():
        def get(self):
            tags = IThemeTagging(self.context).tags
            if len(tags) > 0:
                return tags[0]
            return None
        def set(self, value):
            IThemeTagging(self.context).tags = (value,)
            vocab = getUtility(IVocabularyFactory, 'Allowed themes')
            themes = vocab(self)
        return property(get, set)
    tags = tags()
        
