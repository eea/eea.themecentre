from eea.themecentre.interfaces import IThemeCentre, IThemeRelation
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.event import notify
from zope.component import adapts
from zope.interface import implements
from zope.app.annotation.interfaces import IAnnotations
from zope.app.event.objectevent import ObjectModifiedEvent, Attributes

KEY = 'eea.themecentre.relatedthemecentres'

class ThemeRelationAdapter(object):
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

    def related():
        def get(self):
            anno = IAnnotations(self.context)
            mapping = anno.get(KEY)
            return list(mapping['related'])
        def set(self, value):
            anno = IAnnotations(self.context)
            mapping = anno.get(KEY)
            mapping['related'] = PersistentList(value)
            
            info = Attributes(IThemeRelation, 'related')            
            notify(ObjectModifiedEvent(self.context, info))
        return property(get, set)
    related = related()
