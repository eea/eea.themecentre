from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

def localized_time(time):
    context = getSite()
    translation = getToolByName(context, 'translation_service')

    # sometimes time ends with a 'W'. That violates iso 8601, but
    # we take care of it anyway, pretend it's a 'Z'.
    if isinstance(time, (unicode, str)) and time.endswith('W'):
        time = time[:-1] + 'Z'

    localized_time = translation.ulocalized_time(time, None, context,
            domain='plone')
    return localized_time
