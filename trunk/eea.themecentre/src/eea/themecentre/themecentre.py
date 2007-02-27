from zope.app.component.hooks import getSite
from zope.app.event.objectevent import ObjectEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Acquisition import aq_parent

from eea.themecentre.interfaces import IThemeTagging, IThemeCentre

class PromotedToThemeCentreEvent(ObjectEvent):
    """ A theme tag has been added to an object. """

def promoted(obj, event):
    # obj should be a folder and that's where we're gonna add a news folder
    obj.invokeFactory('Folder', id='news', title='News')
    obj.invokeFactory('Folder', id='events', title='Events')
    obj.invokeFactory('Folder', id='links', title='Links')

    newsobj = getattr(obj, 'news', None)
    eventsobj = getattr(obj, 'events', None)
    linksobj = getattr(obj, 'links', None)

    if newsobj:
        workflow = getToolByName(obj, 'portal_workflow')
        workflow.doActionFor(newsobj, 'publish')
        newsobj.setConstrainTypesMode(1)
        newsobj.setImmediatelyAddableTypes(['News Item'])
        newsobj.setLocallyAllowedTypes(['News Item'])

    if eventsobj:
        workflow = getToolByName(obj, 'portal_workflow')
        workflow.doActionFor(eventsobj, 'publish')
        eventsobj.setConstrainTypesMode(1)
        eventsobj.setImmediatelyAddableTypes(['Event'])
        eventsobj.setLocallyAllowedTypes(['Event'])

    if linksobj:
        workflow = getToolByName(obj, 'portal_workflow')
        workflow.doActionFor(linksobj, 'publish')
        linksobj.setConstrainTypesMode(1)
        linksobj.setImmediatelyAddableTypes(['Link'])
        linksobj.setLocallyAllowedTypes(['Link'])

def getTheme(context):
    """ looks up the closest theme centre """

    while not IPloneSiteRoot.providedBy(context) and \
          not IThemeCentre.providedBy(context):
        context = aq_parent(context)

    if IThemeCentre.providedBy(context):
        themes = IThemeTagging(context)

        if themes:
            return themes.tags

    return None
