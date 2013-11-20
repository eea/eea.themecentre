""" Theme taggable module
"""
from eea.themecentre.interfaces import IThemeTagging, IThemeTaggable
from eea.themecentre.interfaces import IThemeCentre, IMainThemeTagging
from eea.themecentre.interfaces import IThemeCentreSchema
from eea.themecentre.themecentre import PromotedToThemeCentreEvent
from eea.themecentre.themecentre import getThemeCentre
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.utils import getToolByName
from zope.component import adapts, getUtility
from zope.event import notify
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent, Attributes
from zope.schema.interfaces import IVocabularyFactory

KEY = 'eea.themecentre.themetaggable'

def getMergedThemes(context, themes):
    """ Get Merged Themes
    """
    if not themes:
        return themes

    vocabularies = getToolByName(context, 'portal_vocabularies', None)
    root = None
    if vocabularies is not None:
        root = vocabularies.getVocabularyByName('themesmerged')
    if root is None:
        return themes

    extra_themes = []
    synonyms = []
    synObjs = {}
    for obj in root.objectValues():
        theme = obj.Title()
        synonyms.append(theme)
        synObjs[theme] = obj

    for theme in themes:
        if theme in synonyms:
            merged = synObjs[theme]
            for synonym in merged.objectValues():
                synonym = synonym.Title()
                if synonym not in themes and synonym not in extra_themes:
                    extra_themes.append(synonym)

    return themes + extra_themes

def checkTheme(context, themes):
    """ Make sure the object is tagged with the current themecentre
    """
    themecentre = getThemeCentre(context)
    if themecentre:
        themeCentreThemes = IThemeCentreSchema(themecentre)
        if themeCentreThemes.tags:
            tag = themeCentreThemes.tags
            if tag not in themes:
                themes.append(tag)

class ThemeTaggable(object):
    """ Theme Taggable
    """
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

    @property
    def tags(self):
        """ Get tags
        """
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        tags = list(mapping['themes'])
        return getMergedThemes(self.context, tags)

    @tags.setter
    def tags(self, value):
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

    @property
    def nondeprecated_tags(self):
        """ Non deprecated tags
        """
        tags = self.tags
        vocab = getUtility(IVocabularyFactory, 'Allowed themes for edit')
        current_themes = [term.value for term in vocab(self)]
        return [tag for tag in tags if tag in current_themes]


class MainThemeTaggable(ThemeTaggable):
    """ Main Theme Taggable
    """
    implements(IMainThemeTagging)
    adapts(IThemeTaggable)

class ThemeCentreTaggable(object):
    """ Theme Centre Taggable
    """
    implements(IThemeCentreSchema)
    adapts(IThemeCentre)

    def __init__(self, context):
        self.context = context

    def gett(self):
        """ Get tags
        """
        tags = IThemeTagging(self.context).tags
        if len(tags) > 0:
            return tags[0]
        return None
    def sett(self, value):
        """ Set tags
        """
        # if folder didn't have a theme tag earlier we send an event
        # so folders and stuff can be created in the themecentre
        tags = IThemeTagging(self.context).tags
        should_promote = not tags

        IThemeTagging(self.context).tags = (value,)
        if value and should_promote:
            notify(PromotedToThemeCentreEvent(self.context))
        #vocab = getUtility(IVocabularyFactory, 'Allowed themes')
        #themes = vocab(self)

    tags = property(gett, sett)

def tagTranslation(obj, event):
    """ Tag Translation
    """
    canonical = obj.getCanonical()
    IThemeTagging(obj).tags = IThemeTagging(canonical).tags
