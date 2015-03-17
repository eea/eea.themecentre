""" Related module
"""
from eea.themecentre.interfaces import IThemeCentre, IThemeRelation
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.event import notify
from zope.component import adapts
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from zope.lifecycleevent import ObjectModifiedEvent, Attributes


KEY = 'eea.themecentre.relatedthemecentres'

class ThemeRelationAdapter(object):
    """ Theme relation adapter """
    implements(IThemeRelation)
    adapts(IThemeCentre)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            related =  { 'related': PersistentList() }
            mapping = annotations[KEY] = PersistentDict(related)
        self.mapping = mapping

    def getr(self):
        """ Ger related """
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        return list(mapping['related'])

    def setr(self, value):
        """ Set related """
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        mapping['related'] = PersistentList(value)

        info = Attributes(IThemeRelation, 'related')
        notify(ObjectModifiedEvent(self.context, info))

    related = property(getr, setr)
