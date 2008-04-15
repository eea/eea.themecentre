from eea.themecentre.interfaces import IThemeTagging, IThemeTaggable
from eea.themecentre.interfaces import IThemeCentre, IMainThemeTagging
from eea.themecentre.interfaces import IThemeCentreSchema
from eea.themecentre.themecentre import PromotedToThemeCentreEvent
from eea.themecentre.themecentre import getThemeCentre
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.app.annotation.interfaces import IAnnotations
from zope.component import adapts, getUtility
from zope.event import notify
from zope.interface import implements
from zope.app.event.objectevent import ObjectModifiedEvent, Attributes
from zope.app.schema.vocabulary import IVocabularyFactory

KEY = 'eea.themecentre.themetaggable'

def checkTheme(context, themes):
    # make sure the object is tagged with the current themecentre
    themecentre = getThemeCentre(context)
    if themecentre:
        themeCentreThemes = IThemeCentreSchema(themecentre)
        if themeCentreThemes.tags:
            tag = themeCentreThemes.tags
            if tag not in themes:
                themes.append(tag)

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

    def tags():
        def get(self):
            anno = IAnnotations(self.context)
            mapping = anno.get(KEY)
            tags = list(mapping['themes'])
            return tags 
        def set(self, value):
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
        return property(get, set)
    tags = tags()

    def nondeprecated_tags(self):
        tags = self.tags
        vocab = getUtility(IVocabularyFactory, 'Allowed themes for edit')
        current_themes = [term.value for term in vocab(self)]
        return [tag for tag in tags if tag in current_themes]

    nondeprecated_tags = property(nondeprecated_tags)

class MainThemeTaggable(ThemeTaggable):
    implements(IMainThemeTagging)
    adapts(IThemeTaggable)

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
            # if folder didn't have a theme tag earlier we send an event
            # so folders and stuff can be created in the themecentre
            tags = IThemeTagging(self.context).tags
            should_promote = not tags

            IThemeTagging(self.context).tags = (value,)
            if value and should_promote:
                notify(PromotedToThemeCentreEvent(self.context))
            vocab = getUtility(IVocabularyFactory, 'Allowed themes')
            themes = vocab(self)
        return property(get, set)
    tags = tags()

