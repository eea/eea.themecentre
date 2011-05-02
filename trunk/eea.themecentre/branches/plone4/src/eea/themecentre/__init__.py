""" eea.themecentre package """

#TODO: clean up below, plone4
## monkey patch of Zope
#from ZPublisher import HTTPRequest
#from zope.publisher.base import DebugFlags

#HTTPRequest.HTTPRequest.debug = DebugFlags()

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('eea.translations')
