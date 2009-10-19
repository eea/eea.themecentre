# monkey patch of Zope
from ZPublisher import HTTPRequest
from zope.publisher.base import DebugFlags

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('eea.translations')

HTTPRequest.HTTPRequest.debug = DebugFlags()
