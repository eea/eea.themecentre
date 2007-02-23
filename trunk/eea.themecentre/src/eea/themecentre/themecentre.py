from zope.app.component.hooks import getSite
from zope.app.event.objectevent import ObjectEvent
from Products.CMFCore.utils import getToolByName

class PromotedToThemeCentreEvent(ObjectEvent):
    """ A theme tag has been added to an object. """

def promoted(obj, event):
    print "WEEEEEEEEEEEEE"
    # obj should be a folder and that's where we're gonna add a news folder
    obj.invokeFactory('Folder', id='news', title='News')
    newsobj = getattr(obj, 'news', None)

    if newsobj:
        workflow = getToolByName(getSite(), 'portal_workflow')
        workflow.doActionFor(newsobj, 'publish')
